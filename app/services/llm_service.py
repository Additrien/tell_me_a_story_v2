from abc import ABC, abstractmethod
from typing import AsyncGenerator, Dict, Optional
from app.services.conversation_manager import conversation_manager
from app.core.config import settings

class BaseLLMService(ABC):
    def _get_story_prompt(self, user_input: str, language: str, phase: Optional[str] = None, previous_content: Optional[str] = None) -> str:
        """Get the appropriate prompt based on conversation history and story phase"""
        try:
            previous_stories = conversation_manager.get_recent_stories(1)
            previous_story = previous_stories[0].story if previous_stories else None
            
            # If we're in a phased generation
            if phase and settings.ENABLE_PHASED_GENERATION:
                phase_info = settings.STORY_PHASES[phase]
                phase_prompt = f"""
                {phase_info['description']}
                Target length: {phase_info['target_words']} words.
                
                Previous content:
                {previous_content if previous_content else 'This is the start of the story.'}
                
                Continue the story by writing the {phase} phase.
                """
                
                if previous_story:
                    phase_prompt += "\nMaintain consistency with themes and style from previous stories."
            else:
                phase_prompt = ""
                
            return settings.get_story_prompt(
                language=language,
                user_input=user_input,
                previous_story=previous_story,
                phase_prompt=phase_prompt if settings.ENABLE_PHASED_GENERATION else None
            )
        except Exception as e:
            print(f"Error in _get_story_prompt: {str(e)}")
            raise

    async def generate_story_phase(self, user_input: str, phase: str, language: str = "french", previous_content: Optional[str] = None) -> AsyncGenerator[str, None]:
        """Generate a specific phase of the story"""
        if not settings.ENABLE_PHASED_GENERATION:
            raise ValueError("Phased generation is not enabled")
        if phase not in settings.STORY_PHASES:
            raise ValueError(f"Invalid phase: {phase}")
            
        async for chunk in self.generate_story(user_input, language, phase, previous_content):
            yield chunk

    @abstractmethod
    async def generate_story(self, user_input: str, language: str = "french", phase: Optional[str] = None, previous_content: Optional[str] = None) -> AsyncGenerator[str, None]:
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
        elif service_type == "openrouter":
            from app.services.openrouter_llm_service import OpenRouterService
            return OpenRouterService()
        else:
            raise ValueError(f"Unknown LLM service type: {service_type}")

# Default instance using the factory
from app.core.config import settings
llm_service = LLMServiceFactory.create_service(settings.DEFAULT_LLM_SERVICE)
