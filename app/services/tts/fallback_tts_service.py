import io
from typing import AsyncGenerator, Optional
from app.services.tts.tts_service import TTSService
from app.utils.text_cleanup import clean_text_for_tts
import logging

logger = logging.getLogger(__name__)

class FallbackTTSService(TTSService):
    """A fallback TTS service that returns a text message when other services fail"""
    
    def __init__(self):
        logger.warning("Using FallbackTTSService - this is a text-only fallback and does not produce audio")
    
    async def convert_text_to_speech(
        self,
        text: str,
        story_id: str,
        language: str,
        gender: str = "female"
    ) -> AsyncGenerator[bytes, None]:
        """
        Instead of generating audio, this fallback service yields a single message
        indicating that TTS is unavailable.
        """
        # Clean text before processing
        text = clean_text_for_tts(text)
        
        # Log the text that would have been converted to speech
        logger.info(f"FallbackTTSService - Text that would be spoken: {text}")
        
        # Create a simple message indicating TTS is unavailable
        message = {
            "type": "tts_unavailable",
            "text": text,
            "message": "Text-to-speech service is currently unavailable. Please check your API keys or try again later."
        }
        
        # Convert the message to JSON and yield it as bytes
        import json
        yield json.dumps(message).encode('utf-8') 