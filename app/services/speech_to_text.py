import torch
from transformers import WhisperProcessor, WhisperForConditionalGeneration
from pydantic import BaseModel, validator
from app.core.config import settings
from app.core.languages import LANGUAGE_TO_ISO, DEFAULT_LANGUAGE
from typing import Dict, Optional

class AudioInput(BaseModel):
    array: list
    sampling_rate: int
    language: str = DEFAULT_LANGUAGE

    @validator('language')
    def validate_language(cls, v):
        if v in LANGUAGE_TO_ISO:
            return v
        if v in LANGUAGE_TO_ISO.values():
            return v
        raise ValueError(f"Unsupported language: {v}. Must be one of {list(LANGUAGE_TO_ISO.keys())} or their ISO codes")

class SpeechToTextService:
    def __init__(self):
        self.processor: Optional[WhisperProcessor] = None
        self.model: Optional[WhisperForConditionalGeneration] = None
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        
    def initialize(self):
        """Initialize the Whisper model and processor. Call this at application startup."""
        if self.processor is not None:
            return  # Already initialized
            
        print(f"Initializing Whisper model {settings.WHISPER_MODEL} on {self.device}")
        
        self.processor = WhisperProcessor.from_pretrained(settings.WHISPER_MODEL)
        self.model = WhisperForConditionalGeneration.from_pretrained(
            settings.WHISPER_MODEL,
            device_map="auto",
            load_in_8bit=True,  # Simple 8-bit quantization
            torch_dtype=torch.float16,
            low_cpu_mem_usage=True
        )
        print("Whisper model initialized successfully")

    async def transcribe(self, audio: AudioInput) -> str:
        if self.processor is None or self.model is None:
            raise RuntimeError("SpeechToTextService not initialized. Call initialize() first.")
            
        if not audio.array or len(audio.array) == 0:
            raise ValueError("Empty audio input received. Please provide valid audio data.")
            
        language_code = LANGUAGE_TO_ISO.get(audio.language, audio.language)
        
        forced_decoder_ids = self.processor.get_decoder_prompt_ids(language=language_code, task="transcribe")
        self.model.config.forced_decoder_ids = forced_decoder_ids
        
        input_features = self.processor(
            audio.array, 
            sampling_rate=audio.sampling_rate, 
            return_tensors="pt"
        ).input_features.to(device=self.device, dtype=torch.float16)

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