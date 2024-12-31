from fastapi import APIRouter, HTTPException, Query, Request, WebSocket, WebSocketDisconnect
from app.services.audio_recorder import audio_recorder, cleanup_audio_file
from app.services.speech_to_text import speech_to_text_service, AudioInput
from app.api.websockets import story_ws
from app.services.conversation_manager import conversation_manager
import soundfile as sf
import librosa
import uuid
from datetime import datetime

router = APIRouter()

@router.websocket("/ws/story/{client_id}")
async def websocket_story_endpoint(websocket: WebSocket, client_id: str):
    await story_ws.connect(websocket, client_id)
    try:
        while True:
            data = await websocket.receive_json()
            
            if data["type"] == "transcription":
                await story_ws.stream_story(
                    websocket,
                    transcription=data["text"],
                    language=data.get("language", "french")
                )
    except WebSocketDisconnect:
        story_ws.disconnect(client_id)
    except Exception as e:
        print(f"Error in WebSocket connection: {str(e)}")
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
async def start_recording_post(language: str = Query(default="french")):
    try:
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
