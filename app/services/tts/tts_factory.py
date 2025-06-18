from typing import Dict, Optional, Type
from app.core.config import settings
from app.services.tts.tts_service import TTSService
from app.services.tts.fal_tts_service import FalTTSService
from app.services.tts.fallback_tts_service import FallbackTTSService
import os
import logging

logger = logging.getLogger(__name__)

class TTSFactory:
    """Factory for creating and managing TTS service instances"""
    
    _services: Dict[str, Type[TTSService]] = {
        "fal": FalTTSService,
        "fallback": FallbackTTSService,
    }
    
    _instances: Dict[str, TTSService] = {}
    _fallback_instance: Optional[TTSService] = None
    
    @classmethod
    def get_service(cls, service_name: Optional[str] = None) -> TTSService:
        """Get or create a TTS service instance"""
        # First check environment variable, then parameter, then settings
        service_name = os.environ.get('TTS_SERVICE') or service_name or settings.TTS_SERVICE
        
        # Default to fal if the requested service is not available
        if service_name not in cls._services:
            logger.warning(f"Unknown TTS service: {service_name}, using fal instead")
            service_name = "fal"
        else:
            logger.info(f"Using TTS service: {service_name}")
        
        # If explicitly requesting fallback, return it
        if service_name == "fallback":
            if not cls._fallback_instance:
                cls._fallback_instance = FallbackTTSService()
            return cls._fallback_instance
        
        # Try to get or create the requested service
        try:
            if service_name not in cls._instances:
                cls._instances[service_name] = cls._services[service_name]()
            return cls._instances[service_name]
        except Exception as e:
            logger.error(f"Failed to initialize TTS service '{service_name}': {str(e)}")
            logger.warning("Falling back to fallback TTS service")
            
            # Return fallback service
            if not cls._fallback_instance:
                cls._fallback_instance = FallbackTTSService()
            return cls._fallback_instance

    @classmethod
    def reset(cls):
        """Reset all service instances. Call this when configuration changes."""
        cls._instances = {}
        cls._fallback_instance = None

# Create a singleton instance
tts_factory = TTSFactory()
