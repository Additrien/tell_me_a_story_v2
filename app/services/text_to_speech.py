import torch
import soundfile as sf
import numpy as np
import io
from app.core.config import settings
from app.core.languages import get_language_code, get_language_name
from transformers import VitsTokenizer, VitsModel, set_seed

class TextToSpeechService:
    DEFAULT_LANGUAGE = "french"
    
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"Using device: {self.device}")
        self.models = {}
        self.tokenizers = {}
        # Preload French model at startup
        self._preload_default_model()
        
    def _preload_default_model(self):
        """Preload the default French model at startup"""
        print(f"Preloading default {self.DEFAULT_LANGUAGE} model...")
        self._load_model(self.DEFAULT_LANGUAGE)

    def _get_model_id(self, language: str) -> str:
        """Get the model ID for a specific language"""
        lang_code = get_language_code(language).split("-")[0]  # Get ISO 639-1 code
        return f"facebook/mms-tts-{lang_code}"

    def _load_model(self, language: str):
        """Load MMS-TTS model and tokenizer for a specific language"""
        if language in self.models:
            print(f"Using cached model for {language}")
            return
            
        model_id = self._get_model_id(language)
        print(f"Loading MMS-TTS model from: {model_id}")
        
        try:
            self.tokenizers[language] = VitsTokenizer.from_pretrained(model_id)
            self.models[language] = VitsModel.from_pretrained(model_id).to(self.device)
            print(f"Successfully loaded model for {language}")
        except Exception as e:
            raise ValueError(f"Failed to load model for language {language}: {str(e)}")

    async def convert_text_to_speech(self, text: str, language: str = DEFAULT_LANGUAGE) -> bytes:
        try:
            # Load model for the requested language if not already loaded
            if language not in self.models:
                print(f"Model for {language} not loaded. Loading now...")
                self._load_model(language)
            
            # Get current model and tokenizer
            model = self.models[language]
            tokenizer = self.tokenizers[language]
            
            # Tokenize the input text
            inputs = tokenizer(text=text, return_tensors="pt")
            
            # Move inputs to device
            inputs = {k: v.to(self.device) for k, v in inputs.items()}
            
            # Make generation deterministic
            set_seed(555)
            
            # Generate audio
            with torch.no_grad():
                output = model(**inputs)
                audio = output.waveform[0].cpu().numpy()
            
            # Convert to bytes
            buffer = io.BytesIO()
            sf.write(buffer, audio, settings.MMS_SAMPLE_RATE, format='wav')
            buffer.seek(0)
            return buffer.read()
            
        except Exception as e:
            raise ValueError(f"Error generating speech for language {language}: {str(e)}")

text_to_speech_service = TextToSpeechService()