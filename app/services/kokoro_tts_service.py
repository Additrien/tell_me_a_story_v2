import asyncio
import aiofiles
import numpy as np
import sounddevice as sd
import torch
import json
from typing import AsyncGenerator, Optional, List
from pathlib import Path
import time

from app.core.config import settings
from app.services.tts_service import TTSService

# Import directly from the cloned repository
from app.models.kokoro.models import build_model
from app.models.kokoro.kokoro import generate

class KokoroTTSService(TTSService):
    def __init__(self):
        """Initialize the TTS service with Kokoro model"""
        self.device = settings.TTS_DEVICE
        self.model = None
        self.voicepacks = {}
        self.sample_rate = 24000  # Kokoro sample rate
        self._initialize_model()
        print("KokoroTTSService initialized")
    
    def _initialize_model(self):
        """Initialize the Kokoro model and load default voice"""
        try:
            model_dir = settings.TTS_MODEL_PATH
            
            # Load model config and build model
            config_path = model_dir / "config.json"
            with open(config_path) as f:
                config = json.load(f)
            
            # Build model with config
            self.model = build_model(config, self.device)
            
            # Load model weights
            weights = torch.load(model_dir / "kokoro-v0_19.pth", map_location='cpu', weights_only=True)['net']
            for key, state_dict in weights.items():
                assert key in self.model, key
                try:
                    self.model[key].load_state_dict(state_dict)
                except:
                    # Some state dicts might have 'module.' prefix, try removing it
                    state_dict = {k[7:]: v for k, v in state_dict.items()}
                    self.model[key].load_state_dict(state_dict, strict=False)
            
            # Move each component to device
            for key in self.model.keys():
                self.model[key] = self.model[key].to(self.device)
            
            print(f"Loaded Kokoro model from {model_dir}")
            
            # Load default voice
            self._load_voice(settings.TTS_VOICE)
            
        except Exception as e:
            print(f"Failed to initialize Kokoro model: {str(e)}")
            raise
    
    def _load_voice(self, voice_name: str):
        """Load a specific voice pack"""
        try:
            if voice_name not in self.voicepacks:
                voice_path = settings.TTS_MODEL_PATH / "voices" / f"{voice_name}.pt"
                self.voicepacks[voice_name] = torch.load(voice_path, weights_only=True).to(self.device)
                print(f"Loaded voice: {voice_name}")
            return self.voicepacks[voice_name]
        except Exception as e:
            print(f"Failed to load voice {voice_name}: {str(e)}")
            raise
    
    def _chunk_text(self, text: str, max_chars: Optional[int] = None) -> list[str]:
        """Split text into sentences for better TTS quality"""
        sentences = []
        current = ""
        
        # Split on sentence endings
        for part in text.replace("!", ".").replace("?", ".").split("."):
            part = part.strip()
            if not part:
                continue
                
            if len(current) + len(part) < (max_chars or settings.TTS_CHUNK_SIZE):
                current = f"{current}. {part}" if current else part
            else:
                if current:
                    sentences.append(current + ".")
                current = part
                
        if current:
            sentences.append(current + ".")
            
        return sentences

    async def convert_text_to_speech(
        self, 
        text: str,
        story_id: str,
        language: str,
    ) -> AsyncGenerator[bytes, None]:
        """Convert text to speech using Kokoro model"""
        stream = None
        try:
            print("Starting text-to-speech conversion")
            
            # Get voice - for Kokoro we only support English voices
            voice = "af_bella" if language.lower().startswith("en") else "bf"  # af for American, bf for British
            voicepack = self._load_voice(voice)
            
            # Split text into sentences
            sentences = self._chunk_text(text)
            
            # Create audio stream
            stream = sd.OutputStream(
                samplerate=self.sample_rate,
                channels=1,
                dtype=np.int16,
                blocksize=1024,
                latency="low",
            )
            stream.start()
            
            for i, sentence in enumerate(sentences, 1):
                try:
                    print(f"Processing sentence {i}/{len(sentences)}")
                    
                    # Add small delay between sentences
                    if i > 1:
                        await asyncio.sleep(0.1)
                    
                    # Generate audio
                    loop = asyncio.get_event_loop()
                    audio_data, _ = await loop.run_in_executor(
                        None,
                        lambda: generate(
                            self.model,
                            sentence,
                            voicepack,
                            lang=voice[0]  # 'a' for American, 'b' for British
                        )
                    )
                    
                    # Normalize and amplify
                    max_value = np.max(np.abs(audio_data))
                    if max_value > 0:
                        audio_data = (audio_data / max_value) * 0.95
                        audio_data *= 1.5  # Slight amplification
                    
                    # Stream in small chunks for low latency
                    buffer_size = 2048
                    for start_idx in range(0, len(audio_data), buffer_size):
                        chunk = audio_data[start_idx:start_idx + buffer_size]
                        chunk_int16 = (chunk * 32767).astype(np.int16)
                        stream.write(chunk_int16)
                        yield chunk_int16.tobytes()
                        await asyncio.sleep(0)  # Allow other tasks to run
                        
                except asyncio.CancelledError:
                    print("Audio streaming cancelled")
                    return
                except Exception as e:
                    print(f"Error processing sentence {i}: {str(e)}")
                    return
                
            print("Text-to-speech conversion completed successfully")
            
        except Exception as e:
            print(f"Error in text-to-speech conversion: {str(e)}")
            raise ValueError(f"Error generating speech: {str(e)}")
        finally:
            if stream is not None:
                try:
                    stream.stop()
                    stream.close()
                except Exception as e:
                    print(f"Error closing audio stream: {str(e)}") 