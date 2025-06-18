from fastapi import WebSocket, WebSocketDisconnect
from typing import Dict, Optional
import json
from app.services.tts.tts_factory import tts_factory
from app.services.conversation_manager import conversation_manager
from app.core.language_manager import language_manager
from app.core.config import settings
# Remove circular import
# import main
# from app.services.llm.global_service import llm_service
import re
import traceback
import sys

class StoryStreamingWebSocket:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
        self.story_states: Dict[str, Dict] = {}
        
    async def connect(self, websocket: WebSocket, client_id: str):
        await websocket.accept()
        print(f"WebSocket connected: client_id={client_id}")
        self.active_connections[client_id] = websocket
        self.story_states[client_id] = {
            "complete_story": "",
            "current_phase": None,
            "awaiting_interaction": False
        }
        
    def disconnect(self, client_id: str):
        print(f"WebSocket disconnected: client_id={client_id}")
        if client_id in self.active_connections:
            self.active_connections.pop(client_id)
        if client_id in self.story_states:
            self.story_states.pop(client_id)
        
    def _split_into_sentences(self, text: str) -> list[str]:
        """Split text into sentences using regex to handle various punctuation"""
        text = text.strip()
        sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|\!)\s', text)
        return [s.strip() for s in sentences if s.strip()]

    async def _process_story_chunk(self, websocket: WebSocket, chunk: str, phase: Optional[str], language: str, sentence_buffer: str, client_id: str) -> str:
        """Process a chunk of story text, handling both text and audio streaming"""
        try:
            print(f"Processing story chunk: client_id={client_id}, phase={phase}, chunk_length={len(chunk)}")
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
                    print(f"Converting sentence to speech: client_id={client_id}, sentence_length={len(sentence)}")
                    try:
                        async for audio_chunk in tts_factory.get_service().convert_text_to_speech(
                            text=sentence,
                            story_id=client_id,
                            language=language
                        ):
                            # Check if this is a fallback message (JSON) or actual audio bytes
                            try:
                                # Try to decode as JSON (fallback service response)
                                fallback_msg = json.loads(audio_chunk.decode('utf-8'))
                                if isinstance(fallback_msg, dict) and fallback_msg.get("type") == "tts_unavailable":
                                    # Send a message to the client that TTS is unavailable
                                    await websocket.send_json({
                                        "type": "tts_unavailable",
                                        "message": fallback_msg.get("message", "TTS service unavailable"),
                                        "text": fallback_msg.get("text", sentence)
                                    })
                                    # Only send this message once per session
                                    if client_id not in self.story_states or "tts_unavailable_notified" not in self.story_states[client_id]:
                                        if client_id in self.story_states:
                                            self.story_states[client_id]["tts_unavailable_notified"] = True
                            except (UnicodeDecodeError, json.JSONDecodeError):
                                # This is actual audio data, send it as bytes
                                await websocket.send_bytes(audio_chunk)
                    except Exception as tts_error:
                        print(f"TTS error for sentence: {str(tts_error)}")
                        # Send a message to the client that TTS failed for this sentence
                        await websocket.send_json({
                            "type": "tts_error",
                            "message": f"Failed to generate speech: {str(tts_error)}",
                            "text": sentence
                        })
                
                return new_buffer
            return sentence_buffer
        except Exception as e:
            print(f"Error in _process_story_chunk: {str(e)}")
            print(f"Traceback: {traceback.format_exc()}")
            raise

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
        
    async def stream_story(
        self,
        websocket: WebSocket,
        transcription: str,
        language: str,
        client_id: str
    ):
        """Stream story generation to the client"""
        try:
            print(f"Starting story streaming: client_id={client_id}, language={language}, transcription_length={len(transcription)}")
            # Initialize story state if not exists
            if client_id not in self.story_states:
                self.story_states[client_id] = {"complete_story": "", "current_phase": None}
            
            # Get the story generator - reimport to ensure we get the latest instance
            import app.services.llm.global_service
            story_generator = app.services.llm.global_service.llm_service
            
            if not story_generator:
                error_msg = "LLM service not initialized"
                print(f"Error: {error_msg}")
                await websocket.send_json({
                    "type": "error",
                    "message": error_msg
                })
                print(f"Error message sent to client: {error_msg}")
                return
            
            print(f"Using LLM service: {type(story_generator).__name__}")
            
            # Get lexical fields from state if available
            lexical_fields = None
            if client_id in self.story_states:
                lexical_fields = self.story_states[client_id].get("lexical_fields")
                if lexical_fields:
                    print(f"Using lexical fields: {lexical_fields}")

            # Generate story with lexical fields
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
                    async for chunk in story_generator.generate_story_phase(
                        transcription,
                        phase=phase,
                        language=language,
                        previous_content=state["complete_story"] if state["complete_story"] else None,
                        chosen_lexical_fields=lexical_fields
                    ):
                        sentence_buffer = await self._process_story_chunk(
                            websocket, chunk, phase, language, sentence_buffer, client_id
                        )
                        state["complete_story"] += chunk
                    
                    print(f"\nLLM Output ({phase}):")
                    print(f"{state['complete_story']}")
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
                async for chunk in story_generator.generate_story(
                    transcription,
                    language,
                    chosen_lexical_fields=lexical_fields
                ):
                    sentence_buffer = await self._process_story_chunk(
                        websocket, chunk, None, language, sentence_buffer, client_id
                    )
                    state["complete_story"] += chunk
            
            # Process remaining text
            if sentence_buffer:
                if not re.search(r'[.!?]$', sentence_buffer):
                    sentence_buffer += "."
                    state["complete_story"] += "."
                
                try:
                    async for audio_chunk in tts_factory.get_service().convert_text_to_speech(
                        text=sentence_buffer,
                        story_id=client_id,
                        language=language
                    ):
                        # Check if this is a fallback message (JSON) or actual audio bytes
                        try:
                            # Try to decode as JSON (fallback service response)
                            fallback_msg = json.loads(audio_chunk.decode('utf-8'))
                            if isinstance(fallback_msg, dict) and fallback_msg.get("type") == "tts_unavailable":
                                # Send a message to the client that TTS is unavailable
                                await websocket.send_json({
                                    "type": "tts_unavailable",
                                    "message": fallback_msg.get("message", "TTS service unavailable"),
                                    "text": fallback_msg.get("text", sentence_buffer)
                                })
                        except (UnicodeDecodeError, json.JSONDecodeError):
                            # This is actual audio data, send it as bytes
                            await websocket.send_bytes(audio_chunk)
                except Exception as tts_error:
                    print(f"TTS error for final sentence: {str(tts_error)}")
                    # Send a message to the client that TTS failed for this sentence
                    await websocket.send_json({
                        "type": "tts_error",
                        "message": f"Failed to generate speech: {str(tts_error)}",
                        "text": sentence_buffer
                    })
            
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
            print(f"Client disconnected during story streaming: client_id={client_id}")
            raise
        except Exception as e:
            error_msg = str(e)
            print(f"Error in story streaming: {error_msg}")
            print(f"Traceback: {traceback.format_exc()}")
            try:
                await websocket.send_json({
                    "type": "error",
                    "message": error_msg
                })
            except Exception as send_error:
                print(f"Failed to send error message: {str(send_error)}")
            
story_ws = StoryStreamingWebSocket()