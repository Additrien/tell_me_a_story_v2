from fastapi import WebSocket, WebSocketDisconnect
from typing import Dict, Optional
import json
from app.services.llm_service import generate_story
from app.services.text_to_speech import text_to_speech_service
from app.services.conversation_manager import conversation_manager
import re

class StoryStreamingWebSocket:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
        
    async def connect(self, websocket: WebSocket, client_id: str):
        await websocket.accept()
        self.active_connections[client_id] = websocket
        
    def disconnect(self, client_id: str):
        self.active_connections.pop(client_id, None)
        
    def _split_into_sentences(self, text: str) -> list[str]:
        """Split text into sentences using regex to handle various punctuation"""
        text = text.strip()
        sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|\!)\s', text)
        return [s.strip() for s in sentences if s.strip()]
        
    async def stream_story(self, websocket: WebSocket, transcription: str, language: str):
        """Stream story generation and audio through WebSocket"""
        try:
            sentence_buffer = ""
            complete_story = ""
            
            # Send initial message
            await websocket.send_json({
                "type": "status",
                "status": "started",
                "message": "Starting story generation"
            })
            
            # Process story chunks
            async for chunk in generate_story(transcription, language):
                # Send text chunk immediately
                await websocket.send_json({
                    "type": "text",
                    "content": chunk
                })
                
                complete_story += chunk
                sentence_buffer += chunk
                sentences = self._split_into_sentences(sentence_buffer)
                
                if len(sentences) > 1:
                    # Keep last incomplete sentence in buffer
                    sentence_buffer = sentences[-1]
                    
                    # Process complete sentences
                    for sentence in sentences[:-1]:
                        # Convert to audio and send
                        async for audio_chunk in text_to_speech_service.convert_text_to_speech(sentence, language):
                            await websocket.send_bytes(audio_chunk)
                            
            # Process remaining text
            if sentence_buffer:
                if not re.search(r'[.!?]$', sentence_buffer):
                    sentence_buffer += "."
                    complete_story += "."
                    
                async for audio_chunk in text_to_speech_service.convert_text_to_speech(sentence_buffer, language):
                    await websocket.send_bytes(audio_chunk)
                    
            # Store the complete story in history
            conversation_manager.add_story(transcription, complete_story, language)
                    
            # Send completion message
            await websocket.send_json({
                "type": "status",
                "status": "completed",
                "message": "Story generation completed"
            })
            
        except WebSocketDisconnect:
            print(f"Client disconnected during story streaming")
        except Exception as e:
            print(f"Error in story streaming: {str(e)}")
            await websocket.send_json({
                "type": "error",
                "message": str(e)
            })
            
story_ws = StoryStreamingWebSocket() 