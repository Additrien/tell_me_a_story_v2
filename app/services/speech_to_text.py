import torch
from transformers import WhisperProcessor, WhisperForConditionalGeneration
from pydantic import BaseModel, validator
from app.core.config import settings
from typing import Dict

# Mapping des noms de langues vers les codes ISO
LANGUAGE_CODES: Dict[str, str] = {
    "french": "fr",
    "english": "en",
    "spanish": "es",
    "german": "de",
    "italian": "it",
    "portuguese": "pt",
    "dutch": "nl",
    "polish": "pl",
    "russian": "ru",
    "chinese": "zh",
    "japanese": "ja",
    "korean": "ko"
}

class AudioInput(BaseModel):
    array: list
    sampling_rate: int
    language: str = "french"

    @validator('language')
    def validate_language(cls, v):
        if v in LANGUAGE_CODES:
            return v
        if v in LANGUAGE_CODES.values():
            return v
        raise ValueError(f"Unsupported language: {v}. Must be one of {list(LANGUAGE_CODES.keys())} or their ISO codes")

class SpeechToTextService:
    def __init__(self):
        # Using medium model as recommended for better non-English performance
        self.processor = WhisperProcessor.from_pretrained("openai/whisper-medium")
        self.model = WhisperForConditionalGeneration.from_pretrained("openai/whisper-medium")
        self.model.config.forced_decoder_ids = None

    async def transcribe(self, audio: AudioInput) -> str:
        # Validate input
        if not audio.array or len(audio.array) == 0:
            raise ValueError("Empty audio input received. Please provide valid audio data.")
            
        # Convertir le nom de la langue en code ISO si nécessaire
        language_code = LANGUAGE_CODES.get(audio.language, audio.language)
        
        # Set forced decoder ids for the language
        forced_decoder_ids = self.processor.get_decoder_prompt_ids(language=language_code, task="transcribe")
        self.model.config.forced_decoder_ids = forced_decoder_ids
        
        input_features = self.processor(
            audio.array, 
            sampling_rate=audio.sampling_rate, 
            return_tensors="pt"
        ).input_features

        # Create attention mask
        attention_mask = torch.ones_like(input_features)
        
        # Generate with proper language settings
        predicted_ids = self.model.generate(
            input_features,
            attention_mask=attention_mask,
            temperature=0.0
        )
        
        transcription = self.processor.batch_decode(predicted_ids, skip_special_tokens=True)
        return transcription[0].strip()

speech_to_text_service = SpeechToTextService()