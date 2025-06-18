import io
import json
import asyncio
import os
import aiohttp
from typing import AsyncGenerator, Optional, Dict, List
import fal_client
from app.core.languages import LANGUAGE_TO_BCP47, DEFAULT_BCP47
from app.utils.text_cleanup import clean_text_for_tts
from app.services.tts.tts_service import TTSService
from app.core.config import settings
from app.services.tts.voice_data import VOICE_DATA, DEFAULT_VOICES

class FalTTSService(TTSService):
    """Text-to-Speech service using fal.ai API"""
    
    DEFAULT_LANGUAGE = DEFAULT_BCP47
    FAL_MODEL_ID = "fal-ai/playai/tts/dialog"
    
    def __init__(self):
        # The API key is already in the format "key_id:key_secret"
        self.api_key = settings.FAL_API_KEY
        
        # Split the API key into key_id and key_secret
        try:
            key_parts = self.api_key.split(":")
            if len(key_parts) != 2:
                raise ValueError("API key must be in format 'key_id:key_secret'")
            
            self.key_id = key_parts[0]
            self.key_secret = key_parts[1]
            print(f"FAL API key parsed successfully: key_id={self.key_id[:5]}..., key_secret={self.key_secret[:5]}...")
        except Exception as e:
            print(f"Error parsing FAL API key: {str(e)}")
            raise
    
    def _get_language_code(self, language: str) -> str:
        """Convert simple language name to BCP-47 code."""
        return LANGUAGE_TO_BCP47.get(language.lower(), language)
    
    def _get_voice_for_language(self, language_code: str, gender: str = "female") -> str:
        """Get the appropriate voice ID for the language and gender."""
        # Normalize gender to one of our categories
        if gender not in ["male", "female", "neutral"]:
            gender = "female"  # Default to female if unspecified or invalid
            
        # Check if we have voices for this language
        if language_code in VOICE_DATA and VOICE_DATA[language_code]:
            # Check if we have voices for this gender in this language
            if gender in VOICE_DATA[language_code] and VOICE_DATA[language_code][gender]:
                # Get the default voice name for this language and gender
                default_voice_name = DEFAULT_VOICES.get(language_code, {}).get(gender)
                
                # If we have a default voice name and it exists in our voice IDs, use it
                if default_voice_name and default_voice_name in VOICE_DATA[language_code][gender]:
                    return VOICE_DATA[language_code][gender][default_voice_name]
                
                # Otherwise, just use the first voice in the list
                first_voice_name = list(VOICE_DATA[language_code][gender].keys())[0]
                return VOICE_DATA[language_code][gender][first_voice_name]
            
            # If we don't have voices for this gender, try to find any voice for this language
            for alt_gender in ["female", "male", "neutral"]:
                if alt_gender in VOICE_DATA[language_code] and VOICE_DATA[language_code][alt_gender]:
                    first_voice_name = list(VOICE_DATA[language_code][alt_gender].keys())[0]
                    return VOICE_DATA[language_code][alt_gender][first_voice_name]
        
        # Fallback to English US if language not supported
        default_voice_name = DEFAULT_VOICES.get("en-US", {}).get(gender, "Jennifer")
        if gender in VOICE_DATA["en-US"] and default_voice_name in VOICE_DATA["en-US"][gender]:
            return VOICE_DATA["en-US"][gender][default_voice_name]
        
        # Ultimate fallback
        return VOICE_DATA["en-US"]["female"]["Jennifer"]
    
    def _chunk_text(self, text: str, max_chars: Optional[int] = None) -> list[str]:
        """Split long text into manageable chunks"""
        chunks = []
        current_chunk = ""
        max_bytes = max_chars or 1000  # fal.ai has a limit, adjust as needed
        
        for sentence in text.split('. '):
            if len((current_chunk + sentence).encode('utf-8')) > max_bytes:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = sentence
            else:
                current_chunk = f"{current_chunk}. {sentence}" if current_chunk else sentence
                
        if current_chunk:
            chunks.append(current_chunk.strip())
            
        return chunks

    async def convert_text_to_speech(
        self,
        text: str,
        story_id: str,
        language: str,
        gender: str = "female"
    ) -> AsyncGenerator[bytes, None]:
        try:
            # Clean text before processing
            text = clean_text_for_tts(text)
            
            # Get language code
            language_code = self._get_language_code(language)
            
            # Get appropriate voice for the language and gender
            voice_id = self._get_voice_for_language(language_code, gender)
            
            # Split text into chunks
            chunks = self._chunk_text(text)

            # Create a client with our credentials
            async_client = fal_client.AsyncClient(key_id=self.key_id, key_secret=self.key_secret)

            for chunk in chunks:
                if not chunk.strip():
                    continue
                
                # Format the input as a dialog with a single speaker
                formatted_text = f"Speaker 1: {chunk}"
                
                payload = {
                    "input": formatted_text,
                    "voices": [
                        {
                            "voice": voice_id,
                            "turn_prefix": "Speaker 1: "
                        }
                    ],
                    "response_format": "url"
                }
                
                print(f"Sending request to fal.ai API using fal-client")
                print(f"Payload: {json.dumps(payload, indent=2)}")
                
                try:
                    # Submit the request using fal-client with explicit client
                    handler = await async_client.submit(
                        self.FAL_MODEL_ID,
                        arguments=payload
                    )
                    
                    # Get the result
                    result = await handler.get()
                    
                    # Extract audio data from response
                    if "audio" in result and "url" in result["audio"]:
                        audio_url = result["audio"]["url"]
                        
                        # Use aiohttp to download the audio
                        async with aiohttp.ClientSession() as session:
                            async with session.get(audio_url) as audio_response:
                                if audio_response.status == 200:
                                    audio_bytes = await audio_response.read()
                                    yield audio_bytes
                                else:
                                    raise ValueError(f"Failed to download audio from URL: {audio_url}, status: {audio_response.status}")
                    else:
                        raise ValueError(f"Unexpected response format from fal.ai API: {result}")
                
                except Exception as e:
                    print(f"Error with fal-client: {str(e)}")
                    raise ValueError(f"Error with fal-client: {str(e)}")
                    
        except Exception as e:
            print(f"TTS Error: {str(e)}")
            print(f"API Key configured: {'Yes' if self.api_key else 'No'}")
            raise ValueError(f"Error generating speech for language {language}: {str(e)}") 