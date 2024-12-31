from fastapi import APIRouter, HTTPException, Query
from app.services.audio_recorder import audio_recorder, cleanup_audio_file
from app.services.speech_to_text import speech_to_text_service, AudioInput
from app.services.llm_service import generate_story
from app.services.text_to_speech import text_to_speech_service
from app.services.audio_player import play_audio
from app.services.conversation_manager import conversation_manager
from app.core.config import routes_config
import soundfile as sf
import librosa
import numpy as np

router = APIRouter()

@router.get("/audio-devices")
async def list_audio_devices():
    devices = audio_recorder.list_input_devices()
    return {"devices": devices}

@router.post("/start-recording")
async def start_recording(language: str = Query(default="french", description="Language code (e.g. 'french', 'english')")):
    audio_recorder.start_recording(language)
    return {"message": "Recording started", "language": language}

@router.post("/stop-recording")
async def stop_recording():
    audio_file = None
    try:
        audio_file, language = audio_recorder.stop_recording()
        
        # Read the audio file
        audio_data, sample_rate = sf.read(audio_file)
        
        if len(audio_data) == 0:
            raise HTTPException(status_code=400, detail="Recorded audio file is empty")
            
        # Print some debug info
        print(f"USER INPUT: Audio length: {len(audio_data)} samples, Sample rate: {sample_rate}")
        
        # Resample to 16kHz for Whisper
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
        
        story_text = await generate_story(transcription, language)
        audio_output = await text_to_speech_service.convert_text_to_speech(story_text, language)
        await play_audio(audio_output)
        return {"message": "Story processed and played successfully", "transcription": transcription, "story": story_text}
    except Exception as e:
        print(f"Error in stop_recording: {str(e)}")
        raise
    finally:
        if audio_file:  # Only cleanup if audio_file was created
            await cleanup_audio_file(audio_file)

@router.post("/reset-conversation")
async def reset_conversation():
    """Reset the conversation history to start fresh"""
    conversation_manager.clear_history()
    return {"message": "Conversation history cleared"}
