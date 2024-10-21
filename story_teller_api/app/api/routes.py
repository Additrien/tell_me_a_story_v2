from fastapi import APIRouter, HTTPException
from app.services.audio_recorder import record_audio, cleanup_audio_file
from app.services.speech_to_text import speech_to_text_service, AudioInput
from app.services.llm_service import generate_story
from app.services.text_to_speech import convert_text_to_speech
from app.services.audio_player import play_audio
from app.core.config import routes_config
import soundfile as sf

router = APIRouter()

for route in routes_config.get("routes", []):
    @router.post(route["path"])
    async def process_story():
        audio_file = record_audio()
        if not audio_file:
            raise HTTPException(status_code=400, detail="No audio recorded or trigger word not detected")
        
        try:
            audio_data, sample_rate = sf.read(audio_file)
            audio_input = AudioInput(array=audio_data.tolist(), sampling_rate=sample_rate)
            transcription = await speech_to_text_service.transcribe(audio_input)
            
            story_text = await generate_story(transcription)
            audio_output = await convert_text_to_speech(story_text)
            await play_audio(audio_output)
            return {"message": "Story processed and played successfully", "transcription": transcription, "story": story_text}
        finally:
            await cleanup_audio_file(audio_file)
