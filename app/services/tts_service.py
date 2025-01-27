from abc import ABC, abstractmethod
from typing import AsyncGenerator, Optional

class TTSService(ABC):
    """Base class for Text-to-Speech services"""
    
    @abstractmethod
    async def convert_text_to_speech(
        self,
        text: str,
        story_id: str,
        language: str,
    ) -> AsyncGenerator[bytes, None]:
        """Convert text to speech and return audio data as a stream of bytes"""
        pass
    
    @abstractmethod
    def _chunk_text(self, text: str, max_chars: Optional[int] = None) -> list[str]:
        """Split text into manageable chunks for processing"""
        pass 