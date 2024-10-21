import torch
from transformers import WhisperProcessor, WhisperForConditionalGeneration
from pydantic import BaseModel

class AudioInput(BaseModel):
    array: list
    sampling_rate: int

class SpeechToTextService:
    def __init__(self):
        self.processor = WhisperProcessor.from_pretrained("openai/whisper-tiny")
        self.model = WhisperForConditionalGeneration.from_pretrained("openai/whisper-tiny")
        self.model.config.forced_decoder_ids = None

    async def transcribe(self, audio: AudioInput) -> str:
        input_features = self.processor(
            audio.array, 
            sampling_rate=audio.sampling_rate, 
            return_tensors="pt"
        ).input_features

        predicted_ids = self.model.generate(input_features)
        transcription = self.processor.batch_decode(predicted_ids, skip_special_tokens=True)
        return transcription[0]

speech_to_text_service = SpeechToTextService()