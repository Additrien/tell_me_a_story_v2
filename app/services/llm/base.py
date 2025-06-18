from abc import ABC, abstractmethod
from typing import AsyncGenerator, Dict, Optional
from app.services.conversation_manager import conversation_manager
from app.core.config import settings

class BaseLLMService(ABC):
    def _get_story_prompt(
        self,
        user_input: str,
        language: str,
        phase: Optional[str] = None,
        previous_content: Optional[str] = None,
        chosen_lexical_fields: Optional[list] = None
    ) -> str:
        """Get the appropriate prompt based on conversation history and story phase"""
        try:
            previous_stories = conversation_manager.get_recent_stories(1)
            previous_story = previous_stories[0]["content"] if previous_stories else None
            
            # If we're in phased generation and have previous content, use that instead
            if settings.ENABLE_PHASED_GENERATION and previous_content:
                previous_story = previous_content
            
            # Get phase-specific prompt if applicable
            phase_prompt = None
            if phase and settings.ENABLE_PHASED_GENERATION:
                phase_description = settings.STORY_PHASES[phase]["description"]
                phase_prompt = f"{phase} Phase: {phase_description}"
            
            # Format the prompt
            return settings.get_story_prompt(
                language=language,
                user_input=user_input,
                previous_story=previous_story,
                phase_prompt=phase_prompt,
                chosen_lexical_fields=chosen_lexical_fields
            )
        except Exception as e:
            print(f"Error getting story prompt: {str(e)}")
            # Fallback to a simple prompt
            return f"Tell a story in {language} about: {user_input}"

    async def generate_story_phase(
        self,
        user_input: str,
        phase: str,
        language: str = "french",
        previous_content: Optional[str] = None,
        chosen_lexical_fields: Optional[list] = None
    ) -> AsyncGenerator[str, None]:
        """Generate a specific phase of a story"""
        if not settings.ENABLE_PHASED_GENERATION:
            # If phased generation is disabled, just generate a full story
            async for chunk in self.generate_story(user_input, language, chosen_lexical_fields=chosen_lexical_fields):
                yield chunk
            return
        
        # Get the phase-specific prompt
        if settings.DEBUG_PRINT_PHASES:
            print(f"\nGenerating {phase} phase...")
            
        # Generate the story for this phase
        async for chunk in self.generate_story(
            user_input, 
            language, 
            phase=phase, 
            previous_content=previous_content,
            chosen_lexical_fields=chosen_lexical_fields
        ):
            yield chunk

    @abstractmethod
    async def generate_story(
        self,
        user_input: str,
        language: str = "french",
        phase: Optional[str] = None,
        previous_content: Optional[str] = None,
        chosen_lexical_fields: Optional[list] = None
    ) -> AsyncGenerator[str, None]:
        """Generate a story based on user input"""
        pass

class LLMServiceFactory:
    @staticmethod
    def create_service(service_type: str = "gemini") -> "BaseLLMService":
        """Create an LLM service based on the specified type"""
        if service_type == "gemini":
            from app.services.llm.gemini import GeminiLLMService
            return GeminiLLMService()
        elif service_type == "local":
            from app.services.llm.local import LocalLLMService
            return LocalLLMService()
        elif service_type == "openrouter":
            from app.services.llm.openrouter import OpenRouterService
            return OpenRouterService()
        else:
            print(f"Unknown LLM service type: {service_type}, defaulting to Gemini")
            from app.services.llm.gemini import GeminiLLMService
            return GeminiLLMService()