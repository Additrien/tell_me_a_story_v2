from pydantic_settings import BaseSettings
from pydantic import Field
from typing import Optional, Literal, Dict, Any
import os
import torch
from pathlib import Path

class Settings(BaseSettings):
    PROJECT_NAME: str = "Story Teller API"
    VERSION: str = "0.1.0"
    API_V1_STR: str = "/api/v1"
    
    # Debug Configuration
    DEBUG_MODE: bool = True
    DEBUG_PRINT_USER_INPUT: bool = True
    DEBUG_PRINT_LLM_OUTPUT: bool = True
    DEBUG_PRINT_PHASES: bool = True
    
    # Story Generation Configuration
    ENABLE_PHASED_GENERATION: bool = True
    # When enabled, allows user interaction after Rising Action and Climax phases
    ENABLE_INTERACTIVE_PHASES: bool = True
    INTERACTIVE_PHASE_PROMPT: str = """
    Based on the story so far:
    {previous_content}
    
    We're about to begin the {next_phase} phase. What would you like to happen next? You can:
    1. Suggest a direction for the story
    2. Add new characters
    3. Introduce a new challenge
    4. Keep the current direction
    
    Your input will influence how the story continues.
    """
    STORY_PHASES: Dict[str, Dict[str, Any]] = {
        "Exposition": {
            "max_tokens": 650,
            "target_words": "400-500",
            "description": "Set up the story world, introduce main characters, establish the tone and setting. Focus on creating a vivid initial scene that hooks the reader. MUST end with a complete sentence that creates suspense or curiosity. Never end mid-sentence.",
            "interactive_prompt": "What do you think will happen to our characters? What would you like to discover about them?"
        },
        "Rising Action": {
            "max_tokens": 1300,
            "target_words": "800-1000",
            "description": "Develop the conflict, show character relationships evolving, and build tension. Include 2-3 smaller challenges that lead to the main conflict. MUST end with a complete sentence showing characters facing an important choice.",
            "interactive_prompt": "Our heroes face an important choice. What do you think they should do?"
        },
        "Climax": {
            "max_tokens": 975,
            "target_words": "600-750",
            "description": "Present the main conflict and build towards its resolution. Show how characters use what they've learned. MUST end with a complete sentence at a crucial moment of tension.",
            "interactive_prompt": "The crucial moment has arrived! How would you like our heroes to face this challenge?"
        },
        "Resolution": {
            "max_tokens": 325,
            "target_words": "200-250",
            "description": "Wrap up loose ends, show character growth, and leave a lasting message. Provide a satisfying conclusion that reinforces the story's theme and shows how the characters have changed.",
            "interactive_prompt": "What did you learn from this story? What would you do in our heroes' place?"
        }
    }
    
    # Input Method Configuration
    ENABLED_INPUT_METHODS: list[Literal["voice", "text"]] = ["voice", "text"]
    
    # LLM Service Configuration
    LLM_SERVICE: Literal["gemini", "local", "openrouter"] = os.getenv("LLM_SERVICE", "gemini")
    
    # Hugging Face Configuration
    HUGGINGFACE_TOKEN: str = os.getenv("HUGGINGFACE_TOKEN", "")
    
    # OpenRouter Configuration
    OPENROUTER_API_KEY: str
    OPENROUTER_MODEL: str = "nousresearch/hermes-3-llama-3.1-405b"
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
    
    # TTS Configuration
    TTS_SERVICE: Literal["google", "kokoro"] = Field(default="google", env="TTS_SERVICE")
    TTS_DEVICE: str = "cuda" if torch.cuda.is_available() else "cpu"
    TTS_MODEL_PATH: Path = Path("app/models/kokoro")
    TTS_MODEL_WEIGHTS: str = "kokoro-v0_19.pth"
    TTS_VOICE: str = "af"
    TTS_CHUNK_SIZE: int = 1000
    AUDIO_DEBUG_DIR: Path = Path("debug/audio")
    AUDIO_OUTPUT_DIR: Path = Path("output/audio")
    
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

    {phase_prompt}

    STORYTELLING FORMAT:
    - Begin the story {continuation_instruction}
    - No introductions or meta-commentary
    - No addressing the listener directly
    - Write as a continuous narrative
    - For Exposition, Rising Action, and Climax phases only: End with a clear pause point that invites interaction
    - NEVER end a phase mid-sentence
    - Each phase MUST end with a complete thought that creates anticipation

    PHASE ENDINGS (for Exposition, Rising Action, and Climax only):
    - Exposition: End with a complete sentence that creates a clear moment of curiosity (e.g., "Lulu's nose caught an intriguing scent that made her whiskers tingle with excitement.")
    - Rising Action: End with a complete sentence showing a clear choice (e.g., "Lulu had to decide: should she take the risky path through the cat's territory, or the longer route through the dark basement?")
    - Climax: End with a complete sentence at the peak of tension (e.g., "As the cat's shadow loomed closer, Lulu clutched the precious piece of cheese, knowing she had only seconds to make her move.")

    STORY STRUCTURE:
    - {story_start_instruction}
    - Build tension and challenges appropriate to the story's genre and theme
    - Include moments that showcase the main character's defining traits
    - End with a resolution that fits the story's tone and theme

    FAILURE PENALTY:
    - If you fail to end the Exposition, Rising Action, or Climax phase with a complete sentence as described, your response will be discarded and you will have to generate it again.
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
    - Use ONLY these punctuation marks: period (.), comma (,), question mark (?), exclamation mark (!), and simple quotes (")
    - Write all numbers as words (e.g., "two" instead of "2")
    - Use complete words, no abbreviations
    - For dialogue, use only simple quotation marks: "Hello," said Tom.
    - NO special characters: no asterisks (*), no dashes (-), no parentheses, no brackets, no ellipsis (...)
    - NO sound effects in text (like *bang*, *whoosh*, etc.)
    - NO text formatting markers (*, _, ~, ^)
    - Write sound effects as part of the narrative (e.g., "There was a loud knock at the door" instead of "*knock knock*")

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
        previous_story: str | None = None,
        phase_prompt: str | None = None
    ) -> str:
        """Format the story prompt with the given parameters."""
        try:
            print(f"DEBUG - Settings.get_story_prompt called with language={language}")
            
            if phase_prompt and "Exposition" in phase_prompt:
                previous_story_section = "This is a new story request. Create an original story based on the child's input."
                continuation_instruction = "with a fresh narrative"
                story_start_instruction = "Start with a strong hook"
            elif phase_prompt and "Rising Action" in phase_prompt:
                previous_story_section = "Now that the scene is set, develop the story further."
                continuation_instruction = "by building upon the established foundation"
                story_start_instruction = "Expand on the existing elements"
            elif phase_prompt and "Climax" in phase_prompt:
                previous_story_section = "The story has built up tension, now bring it to its peak."
                continuation_instruction = "by elevating the conflict"
                story_start_instruction = "Drive the story towards its climactic moment"
            elif phase_prompt and "Resolution" in phase_prompt:
                previous_story_section = "The climax has occurred, now bring the story to a satisfying close."
                continuation_instruction = "by wrapping up all story elements"
                story_start_instruction = "Guide the story to its conclusion"
            elif previous_story:
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
                story_start_instruction=story_start_instruction,
                phase_prompt=phase_prompt or ""
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
