from fastapi import WebSocket, WebSocketDisconnect
from typing import Dict, Optional
import json
from app.services.llm_service import llm_service
from app.services.text_to_speech import text_to_speech_service
from app.services.conversation_manager import conversation_manager
from app.core.language_manager import language_manager
from app.core.config import settings
import re

class StoryStreamingWebSocket:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
        self.story_states: Dict[str, Dict] = {}
        
    async def connect(self, websocket: WebSocket, client_id: str):
        await websocket.accept()
        self.active_connections[client_id] = websocket
        self.story_states[client_id] = {
            "complete_story": "",
            "current_phase": None,
            "awaiting_interaction": False
        }
        
    def disconnect(self, client_id: str):
        if client_id in self.active_connections:
            self.active_connections.pop(client_id)
        if client_id in self.story_states:
            self.story_states.pop(client_id)
        
    def _split_into_sentences(self, text: str) -> list[str]:
        """Split text into sentences using regex to handle various punctuation"""
        text = text.strip()
        sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|\!)\s', text)
        return [s.strip() for s in sentences if s.strip()]

    async def _process_story_chunk(self, websocket: WebSocket, chunk: str, phase: Optional[str], language: str, sentence_buffer: str) -> tuple[str, str]:
        """Process a chunk of story text, handling both text and audio streaming"""
        await websocket.send_json({
            "type": "text",
            "content": chunk,
            "phase": phase
        })
        
        sentence_buffer += chunk
        sentences = self._split_into_sentences(sentence_buffer)
        
        if len(sentences) > 1:
            # Keep last incomplete sentence in buffer
            new_buffer = sentences[-1]
            
            # Process complete sentences
            for sentence in sentences[:-1]:
                async for audio_chunk in text_to_speech_service.convert_text_to_speech(sentence, language):
                    await websocket.send_bytes(audio_chunk)
            
            return new_buffer
        return sentence_buffer

    async def _request_user_interaction(self, websocket: WebSocket, client_id: str, next_phase: str) -> str:
        """Request and wait for user interaction between phases"""
        state = self.story_states[client_id]
        prompt = settings.INTERACTIVE_PHASE_PROMPT.format(
            previous_content=state["complete_story"],
            next_phase=next_phase
        )
        
        # Send interaction request
        await websocket.send_json({
            "type": "interaction_request",
            "message": prompt,
            "phase_prompt": settings.STORY_PHASES[next_phase]["interactive_prompt"]
        })
        
        # Wait for user response
        state["awaiting_interaction"] = True
        while state["awaiting_interaction"]:
            try:
                response = await websocket.receive_json()
                if response["type"] == "interaction_response":
                    state["awaiting_interaction"] = False
                    return response["content"]
            except WebSocketDisconnect:
                raise
        
        return ""  # Fallback in case of issues
        
    async def stream_story(self, websocket: WebSocket, transcription: str, language: str = None, client_id: str = None):
        """Stream story generation and audio through WebSocket"""
        try:
            language = language or language_manager.current_language
            state = self.story_states.get(client_id, {
                "complete_story": "",
                "current_phase": None,
                "awaiting_interaction": False
            })
            sentence_buffer = ""
            
            # Debug: Print initial user input
            print("\n=== Story Generation Start ===")
            print(f"Initial User Input: {transcription}")
            print(f"Language: {language}")
            
            # Send initial message with language
            await websocket.send_json({
                "type": "status",
                "status": "started",
                "message": "Starting story generation",
                "language": language
            })
            
            if settings.ENABLE_PHASED_GENERATION:
                phases = list(settings.STORY_PHASES.keys())
                for i, phase in enumerate(phases):
                    state["current_phase"] = phase
                    print(f"\n=== Phase {i+1}: {phase} ===")
                    
                    # Process story chunks for this phase
                    generator = llm_service.generate_story_phase(
                        transcription, 
                        phase=phase,
                        language=language,
                        previous_content=state["complete_story"] if state["complete_story"] else None
                    )
                    
                    phase_output = ""
                    async for chunk in generator:
                        sentence_buffer = await self._process_story_chunk(
                            websocket, chunk, phase, language, sentence_buffer
                        )
                        state["complete_story"] += chunk
                        phase_output += chunk
                    
                    print(f"\nLLM Output ({phase}):")
                    print(f"{phase_output}")
                    print(f"=== End of {phase} ===\n")

                    # Request user interaction after Exposition, Rising Action, and Climax
                    if settings.ENABLE_INTERACTIVE_PHASES and i < 3:  # All phases except Resolution
                        next_phase = phases[i + 1]  # Get the name of the next phase
                        user_input = await self._request_user_interaction(websocket, client_id, next_phase)
                        if user_input:
                            print(f"\nUser Interaction Input (before {next_phase}):")
                            print(f"{user_input}")
                            transcription = f"{transcription}\n\nFor the {next_phase} phase: {user_input}"
            else:
                # Process story chunks without phases
                story_output = ""
                async for chunk in llm_service.generate_story(transcription, language):
                    sentence_buffer = await self._process_story_chunk(
                        websocket, chunk, None, language, sentence_buffer
                    )
                    state["complete_story"] += chunk
                    story_output += chunk
                
                print("\nLLM Output (No Phases):")
                print(f"{story_output}")
            
            # Process remaining text
            if sentence_buffer:
                if not re.search(r'[.!?]$', sentence_buffer):
                    sentence_buffer += "."
                    state["complete_story"] += "."
                    
                async for audio_chunk in text_to_speech_service.convert_text_to_speech(sentence_buffer, language):
                    await websocket.send_bytes(audio_chunk)
                    
            # Store the complete story in history
            conversation_manager.add_story(transcription, state["complete_story"], language)
            
            print("\n=== Story Generation Complete ===")
            print(f"Final story length: {len(state['complete_story'])} characters")
                    
            # Send completion message
            await websocket.send_json({
                "type": "status",
                "status": "completed",
                "message": "Story generation completed"
            })
            
        except WebSocketDisconnect:
            print(f"Client disconnected during story streaming")
            raise
        except Exception as e:
            print(f"Error in story streaming: {str(e)}")
            await websocket.send_json({
                "type": "error",
                "message": str(e)
            })
            
story_ws = StoryStreamingWebSocket()