from abc import ABC, abstractmethod
from typing import AsyncGenerator
from app.services.conversation_manager import conversation_manager
from app.core.config import settings

class BaseLLMService(ABC):
    def _get_story_prompt(self, user_input: str, language: str) -> str:
        """Get the appropriate prompt based on conversation history"""
        try:
            print("DEBUG - Starting _get_story_prompt")
            previous_stories = conversation_manager.get_recent_stories(1)
            previous_story = previous_stories[0].story if previous_stories else None
            print(f"DEBUG - Previous story retrieved: {previous_story is not None}")
            
            print("DEBUG - About to call settings.get_story_prompt")
            prompt = settings.get_story_prompt(
                language=language,
                user_input=user_input,
                previous_story=previous_story
            )
            print("DEBUG - Successfully got story prompt")
            return prompt
        except Exception as e:
            print(f"DEBUG - Error in _get_story_prompt: {str(e)}")
            raise

    @abstractmethod
    async def generate_story(self, user_input: str, language: str = "french") -> AsyncGenerator[str, None]:
        """Generate a story based on user input and language.
        This method should use _get_story_prompt to get the appropriate prompt."""
        pass

class LLMServiceFactory:
    @staticmethod
    def create_service(service_type: str = "gemini") -> BaseLLMService:
        if service_type == "gemini":
            from app.services.gemini_llm_service import GeminiLLMService
            return GeminiLLMService()
        elif service_type == "local":
            from app.services.local_llm_service import LocalLLMService
            return LocalLLMService()
        else:
            raise ValueError(f"Unknown LLM service type: {service_type}")

# Default instance using the factory
from app.core.config import settings
llm_service = LLMServiceFactory.create_service(settings.DEFAULT_LLM_SERVICE)
