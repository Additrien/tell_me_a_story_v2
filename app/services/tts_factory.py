from typing import Dict, Optional, Type
from app.core.config import settings
from app.services.tts_service import TTSService
from app.services.kokoro_tts_service import KokoroTTSService
from app.services.google_tts_service import GoogleTextToSpeechService

class TTSFactory:
    """Factory for creating and managing TTS service instances"""
    
    _services: Dict[str, Type[TTSService]] = {
        "kokoro": KokoroTTSService,
        "google": GoogleTextToSpeechService,
    }
    
    _instances: Dict[str, TTSService] = {}
    
    @classmethod
    def get_service(cls, service_name: Optional[str] = None) -> TTSService:
        """Get or create a TTS service instance"""
        service_name = service_name or settings.TTS_SERVICE
        print(f"Using TTS service: {service_name} (configured: {settings.TTS_SERVICE})")
        
        if service_name not in cls._services:
            raise ValueError(f"Unknown TTS service: {service_name}")
        
        if service_name not in cls._instances:
            cls._instances[service_name] = cls._services[service_name]()
        
        return cls._instances[service_name]

    @classmethod
    def reset(cls):
        """Reset all service instances. Call this when configuration changes."""
        cls._instances = {}
tts_factory = TTSFactory()
