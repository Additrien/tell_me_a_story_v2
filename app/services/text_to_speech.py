from google.cloud import texttospeech
import io
from app.core.languages import LANGUAGE_TO_BCP47, TTS_VOICES, DEFAULT_BCP47

class TextToSpeechService:
    DEFAULT_LANGUAGE = DEFAULT_BCP47
    
    def __init__(self):
        self.client = texttospeech.TextToSpeechClient()
        self.voices = TTS_VOICES

    def _get_language_code(self, language: str) -> str:
        """Convert simple language name to BCP-47 code."""
        return LANGUAGE_TO_BCP47.get(language.lower(), language)

    def _chunk_text(self, text: str, max_bytes: int = 4500) -> list[str]:
        """Split long text into manageable chunks"""
        chunks = []
        current_chunk = ""
        
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

    async def convert_text_to_speech(self, text: str, language: str = DEFAULT_LANGUAGE) -> bytes:
        try:
            language_code = self._get_language_code(language)
            chunks = self._chunk_text(text)
            audio_chunks = []

            for chunk in chunks:
                input_text = texttospeech.SynthesisInput(text=chunk)
                
                voice = texttospeech.VoiceSelectionParams(
                    language_code=language_code,
                    name=self.voices.get(language_code, self.voices["fr-FR"])
                )

                audio_config = texttospeech.AudioConfig(
                    audio_encoding=texttospeech.AudioEncoding.LINEAR16,
                    sample_rate_hertz=16000
                )

                response = self.client.synthesize_speech(
                    input=input_text,
                    voice=voice,
                    audio_config=audio_config
                )
                
                audio_chunks.append(response.audio_content)

            return b''.join(audio_chunks)
            
        except Exception as e:
            raise ValueError(f"Error generating speech for language {language}: {str(e)}")

text_to_speech_service = TextToSpeechService()