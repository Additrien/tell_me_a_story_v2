from fastapi import APIRouter, HTTPException, Query, Request, WebSocket, WebSocketDisconnect, Body
from app.services.audio_recorder import audio_recorder, cleanup_audio_file
from app.services.speech_to_text import speech_to_text_service, AudioInput
from app.api.websockets import story_ws
from app.services.conversation_manager import conversation_manager
from app.core.config import settings
from app.services.tts.tts_factory import tts_factory, TTSFactory
import soundfile as sf
import librosa
import uuid
from datetime import datetime
from app.core.languages import LANGUAGE_TO_BCP47, DEFAULT_LANGUAGE, LANGUAGE_TO_ISO
from app.core.language_manager import language_manager
from typing import List, Dict, Any, Optional
from app.services.llm.global_service import llm_service

router = APIRouter()

def validate_input_method(method: str):
    if method not in settings.ENABLED_INPUT_METHODS:
        raise HTTPException(
            status_code=400,
            detail=f"Input method '{method}' is not enabled. Enabled methods: {settings.ENABLED_INPUT_METHODS}"
        )

@router.websocket("/ws/story/{client_id}")
async def websocket_story_endpoint(websocket: WebSocket, client_id: str):
    print(f"\n=== WebSocket Connection Request ===")
    print(f"Client ID: {client_id}")
    
    await story_ws.connect(websocket, client_id)
    try:
        while True:
            print(f"Waiting for message from client: {client_id}")
            data = await websocket.receive_json()
            print(f"Received message from client {client_id}: {data}")
            
            if data["type"] == "transcription":
                print(f"Processing transcription request: client_id={client_id}, language={data.get('language', 'french')}")
                await story_ws.stream_story(
                    websocket,
                    transcription=data["text"],
                    language=data.get("language", "french"),
                    client_id=client_id
                )
            elif data["type"] == "interaction_response" and story_ws.story_states.get(client_id, {}).get("awaiting_interaction"):
                print(f"Received interaction response: client_id={client_id}")
                # Handle user interaction response
                continue  # The _request_user_interaction method will handle this
            else:
                print(f"Unknown message type or not awaiting interaction: {data}")
    except WebSocketDisconnect:
        print(f"WebSocket disconnected: client_id={client_id}")
        story_ws.disconnect(client_id)
    except Exception as e:
        print(f"Error in WebSocket connection: {str(e)}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")
        story_ws.disconnect(client_id)

@router.get("/stories")
async def get_story_history(limit: int = Query(default=5, ge=1, le=20)):
    """Get recent story history"""
    stories = conversation_manager.get_recent_stories(limit)
    return [{
        "transcription": story.transcription,
        "story": story.story,
        "language": story.language,
        "timestamp": story.timestamp.isoformat()
    } for story in stories]

@router.post("/stories/clear")
async def clear_story_history():
    """Clear story history"""
    conversation_manager.clear_history()
    return {"message": "Story history cleared"}

@router.post("/start-recording")
async def start_recording_post(language: str = Query(default=None)):
    validate_input_method("voice")
    try:
        language = language or language_manager.current_language
        audio_recorder.start_recording(language)
        return {"status": "recording_started"}
    except Exception as e:
        print(f"Error in start_recording: {str(e)}")
        raise

@router.post("/stop-recording")
async def stop_recording_post(request: Request, language: str = Query(default="french")):
    audio_file = None
    try:
        audio_file, language = audio_recorder.stop_recording()
        
        audio_data, sample_rate = sf.read(audio_file)
        if len(audio_data) == 0:
            raise HTTPException(status_code=400, detail="Recorded audio file is empty")
            
        print(f"USER INPUT: Audio length: {len(audio_data)} samples, Sample rate: {sample_rate}")
        
        resampled_audio = librosa.resample(audio_data, orig_sr=sample_rate, target_sr=16000)
        
        audio_input = AudioInput(
            array=resampled_audio.tolist(), 
            sampling_rate=16000,
            language=language
        )
        
        transcription = await speech_to_text_service.transcribe(audio_input)
        if not transcription or transcription.isspace():
            raise HTTPException(status_code=400, detail="Failed to transcribe audio - no text detected")
            
        print(f"TRANSCRIPTION: {transcription}")
        
        client_id = str(uuid.uuid4())
        return {
            "transcription": transcription,
            "client_id": client_id,
            "websocket_url": f"/api/v1/ws/story/{client_id}"
        }

    except Exception as e:
        print(f"Error in stop_recording: {str(e)}")
        raise
    finally:
        if audio_file:
            await cleanup_audio_file(audio_file)

@router.post("/text-input")
async def text_input(
    request: Request,
    text: str = Body(...),
    lexical_fields: List[str] | None = Body(None),
    language: str = Query(default=None)
):
    try:
        print(f"\n=== Text Input Request ===")
        print(f"Text: {text[:100]}{'...' if len(text) > 100 else ''}")
        print(f"Language: {language}")
        print(f"Lexical fields: {lexical_fields}")
        
        validate_input_method("text")
        if not text or text.isspace():
            print("Error: Empty text input")
            raise HTTPException(status_code=400, detail="Text input cannot be empty")
            
        language = language or language_manager.current_language
        client_id = str(uuid.uuid4())
        print(f"Generated client_id: {client_id}")
        
        # Store lexical fields in story_ws state for this client
        if lexical_fields:
            story_ws.story_states[client_id] = {"lexical_fields": lexical_fields}
        
        response_data = {
            "transcription": text,
            "client_id": client_id,
            "websocket_url": f"/api/v1/ws/story/{client_id}"
        }
        print(f"Response: {response_data}")
        return response_data
    except Exception as e:
        print(f"Error in text_input: {str(e)}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")
        raise

@router.get("/languages")
async def get_languages():
    """Get available languages and their codes"""
    return {
        "available_languages": list(LANGUAGE_TO_BCP47.keys()),
        "default_language": DEFAULT_LANGUAGE
    }

@router.post("/language")
async def set_language(language: str = Body(..., embed=True)):
    """Set the current language"""
    if language not in LANGUAGE_TO_BCP47:
        raise HTTPException(
            status_code=400, 
            detail=f"Unsupported language. Available languages: {list(LANGUAGE_TO_BCP47.keys())}"
        )
    language_manager.set_language(language)
    return {"language": language}

@router.post("/reload-config")
async def reload_config():
    """Reload configuration and reset services"""
    settings.Config.env_file = ".env"
    tts_factory.reset()
    return {"message": "Configuration reloaded and services reset"}

@router.post("/tts-service")
async def set_tts_service(service: str = Body(..., embed=True)):
    """Set the TTS service to use"""
    if service not in ["fal"]:
        raise HTTPException(
            status_code=400,
            detail=f"Unknown TTS service: {service}. Available services: fal"
        )
    
    # Set environment variable
    import os
    os.environ['TTS_SERVICE'] = service
    
    # Reset TTS factory to use new service
    tts_factory.reset()
    
    return {"message": f"TTS service set to {service}"}

@router.get("/tts-service")
async def get_tts_service():
    """Get the current TTS service and available services"""
    import os
    current_service = os.environ.get('TTS_SERVICE') or settings.TTS_SERVICE
    available_services = list(tts_factory._services.keys())
    
    return {
        "current_service": current_service,
        "available_services": available_services
    }

@router.get("/lexical-fields")
async def get_lexical_fields() -> Dict[str, Dict[str, Any]]:
    """Get available lexical fields for story generation based on deployment type."""
    return settings.get_available_lexical_fields()

@router.post("/story/generate")
async def generate_story(user_input: str, language: str = "french"):
    """Generate a story based on user input"""
    if not llm_service:
        raise HTTPException(status_code=500, detail="LLM service not initialized")
    
    # Generate story
    async for chunk in llm_service.generate_story(user_input, language):
        yield chunk

@router.websocket("/story/stream")
async def stream_story(websocket: WebSocket):
    """Stream story generation to the client"""
    await websocket.accept()
    
    if not llm_service:
        await websocket.send_json({"error": "LLM service not initialized"})
        return
