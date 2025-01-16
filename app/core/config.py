from pydantic_settings import BaseSettings
from typing import Optional, Literal
import os

class Settings(BaseSettings):
    PROJECT_NAME: str = "Story Teller API"
    VERSION: str = "0.1.0"
    API_V1_STR: str = "/api/v1"
    
    # Input Method Configuration
    ENABLED_INPUT_METHODS: list[Literal["voice", "text"]] = ["voice", "text"]
    
    # LLM Service Configuration
    DEFAULT_LLM_SERVICE: Literal["gemini", "local", "openrouter"] = os.getenv("LLM_SERVICE", "gemini")
    
    # Hugging Face Configuration
    HUGGINGFACE_TOKEN: str = os.getenv("HUGGINGFACE_TOKEN", "")
    
    # OpenRouter Configuration
    OPENROUTER_API_KEY: str
    OPENROUTER_MODEL: str = "anthropic/claude-3-opus-20240229"
    OPENROUTER_BASE_URL: str = "https://openrouter.ai/api/v1"
    OPENROUTER_MAX_TOKENS: int = 2048
    OPENROUTER_TEMPERATURE: float = 0.7
    OPENROUTER_TOP_P: float = 0.8
    OPENROUTER_FREQUENCY_PENALTY: float = 0.0
    OPENROUTER_PRESENCE_PENALTY: float = 0.0
    
    # Whisper Configuration
    WHISPER_MODEL: str = "openai/whisper-small"
    
    # Gemini Configuration
    GEMINI_API_KEY: str
    GEMINI_MODEL: str = "gemini-2.0-flash-exp"
    GEMINI_MAX_OUTPUT_TOKENS: int = 2048
    GEMINI_TEMPERATURE: float = 0.7
    GEMINI_TOP_P: float = 0.8
    GEMINI_TOP_K: int = 40
    
    # Audio Configuration
    AUDIO_DEVICE_INDEX: Optional[int] = 7
    TTS_SAMPLE_RATE: int = 16000
    
    # Google Cloud Configuration
    google_application_credentials: str
    google_cloud_project: str
    
    # Story Configuration
    STORY_PROMPT_TEMPLATE: str = """
    You are a master storyteller for young children aged 6 years old.

    STRICT LANGUAGE RULE:
    You MUST write ONLY in {language}. No other language is allowed.
    - French for "french"
    - English for "english"
    - Spanish for "spanish"

    {previous_story_section}

    STORYTELLING FORMAT:
    - Begin the story {continuation_instruction}
    - No introductions or meta-commentary
    - No addressing the listener directly
    - No questions to the audience
    - Write as a continuous narrative

    STORY STRUCTURE:
    - Length: 20-25 sentences
    - One flowing story without sections
    - {story_start_instruction}
    - Build tension and challenges appropriate to the story's genre and theme
    - Include moments that showcase the main character's defining traits
    - End with a resolution that fits the story's tone and theme

    GENRE ADAPTATION:
    - Identify the core genre from the user's request
    - Match narrative style to genre expectations
    - Scale conflict and action to genre conventions
    - Use appropriate vocabulary and tone
    - Maintain genre-specific story beats
    - Honor genre tropes while keeping age-appropriate

    CHARACTER DEVELOPMENT:
    - Establish character traits early
    - Show character abilities consistently
    - Build challenges that test the character
    - Demonstrate growth through actions
    - Keep powers/abilities consistent throughout
    - Match character actions to their established nature

    WRITING STYLE:
    - Match vocabulary to story context
    - Use vivid, age-appropriate descriptions
    - Balance action and character moments
    - Create immersive scenes
    - Keep consistent tone throughout

    EMOTIONAL JOURNEY:
    - Create stakes that matter to the character
    - Build tension naturally
    - Include moments of triumph
    - Show character relationships
    - Maintain emotional authenticity

    TEXT-TO-SPEECH FORMATTING:
    - Standard punctuation only (. , ?)
    - Numbers as words
    - Full words (no abbreviations)
    - Simple quotation marks for dialogue
    - No special characters or sound effects
    - No text formatting or emphasis markers

    CONTENT RULES:
    - Age-appropriate content only
    - No graphic elements
    - Focus on positive themes
    - Keep intensity manageable for young children
    - Celebrate character virtues

    CHILD'S INPUT:
    "{user_input}"
    """
    
    @property
    def STORY_PROMPT(self) -> str:
        return self.STORY_PROMPT_TEMPLATE
    
    def get_story_prompt(
        self,
        language: str,
        user_input: str,
        previous_story: str | None = None
    ) -> str:
        """Format the story prompt with the given parameters."""
        try:
            print(f"DEBUG - Settings.get_story_prompt called with language={language}")
            
            if previous_story:
                previous_story_section = f"""
                PREVIOUS STORY:
                {previous_story}
                
                This is a follow-up request. Continue with the same universe and characters, maintaining consistency with the previous story.
                """
                continuation_instruction = "by continuing the adventure"
                story_start_instruction = "Pick up where we left off"
            else:
                previous_story_section = "This is a new story request. Create an original story based on the child's input."
                continuation_instruction = "with a fresh narrative"
                story_start_instruction = "Start with a strong hook"
            
            print("DEBUG - About to format prompt template")
            formatted_prompt = self.STORY_PROMPT.format(
                language=language,
                user_input=user_input,
                previous_story_section=previous_story_section,
                continuation_instruction=continuation_instruction,
                story_start_instruction=story_start_instruction
            )
            print("DEBUG - Successfully formatted prompt")
            return formatted_prompt
        except Exception as e:
            print(f"DEBUG - Error in Settings.get_story_prompt: {str(e)}")
            print(f"DEBUG - Error type: {type(e)}")
            raise

    # Llama Configuration
    LLAMA_MAX_NEW_TOKENS: int = 2048
    LLAMA_TEMPERATURE: float = 0.7
    LLAMA_TOP_P: float = 0.8
    LLAMA_TOP_K: int = 40
        
    class Config:
        env_file = ".env"

settings = Settings()

