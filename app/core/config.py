from pydantic_settings import BaseSettings
from pydantic import Field
from typing import Optional, Literal, Dict, Any, ClassVar
import os
import torch
from pathlib import Path
import yaml

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
    TTS_SERVICE: Literal["fal"] = Field(default="fal", env="TTS_SERVICE")
    TTS_DEVICE: str = "cuda" if torch.cuda.is_available() else "cpu"
    TTS_CHUNK_SIZE: int = 1000
    AUDIO_DEBUG_DIR: Path = Path("debug/audio")
    AUDIO_OUTPUT_DIR: Path = Path("output/audio")
    
    # Fal.ai Configuration
    FAL_API_KEY: str = os.getenv("FAL_API_KEY", "")
    
    # Google Cloud Configuration
    google_application_credentials: str
    google_cloud_project: str
    
    # Deployment Configuration
    DEPLOYMENT_TYPE: Literal["children", "adults"] = Field(
        default="children",
        env="DEPLOYMENT_TYPE",
        description="Type of deployment - determines available content and features"
    )
    
    # Llama Configuration
    LLAMA_MAX_NEW_TOKENS: int = 2048
    LLAMA_TEMPERATURE: float = 0.7
    LLAMA_TOP_P: float = 0.8
    LLAMA_TOP_K: int = 40

    # Play.AI Configuration
    PLAY_USER_ID: str = ""
    PLAY_SECRET_KEY: str = ""
    
    def _load_prompt_template(self) -> Dict[str, Any]:
        """Load and merge common and specific prompt templates."""
        try:
            # Load common prompt template
            with open("config/common_prompt.yaml", 'r') as f:
                common_config = yaml.safe_load(f)['common']

            # Load specific prompt template
            config_file = f"config/{self.DEPLOYMENT_TYPE}_prompt.yaml"
            with open(config_file, 'r') as f:
                specific_config = yaml.safe_load(f)['story_prompt']

            # Merge format rules if they exist in both
            if 'format_rules' in specific_config:
                # Keep only specific rules, common rules will be referenced in template
                specific_config['format_rules'] = specific_config['format_rules']

            # Merge writing style if it exists in both
            if 'writing_style' in specific_config:
                # Keep only specific rules, common rules will be referenced in template
                specific_config['writing_style'] = specific_config['writing_style']

            # Merge TTS formatting rules if they exist in both
            if 'tts_formatting' in specific_config:
                # Keep only specific rules, common rules will be referenced in template
                specific_config['tts_formatting'] = {
                    'rules': specific_config['tts_formatting']['rules']
                }

            return specific_config
        except Exception as e:
            print(f"Error loading prompt template: {str(e)}")
            raise

    def get_available_lexical_fields(self) -> Dict[str, Dict[str, Any]]:
        """Get all available lexical fields for the current deployment type."""
        prompt_config = self._load_prompt_template()
        return prompt_config.get('lexical_fields', {})

    def get_story_prompt(
        self,
        language: str,
        user_input: str,
        previous_story: Optional[str] = None,
        phase_prompt: Optional[str] = None,
        chosen_lexical_fields: Optional[list] = None
    ) -> str:
        """Format the story prompt with the given parameters."""
        try:
            print(f"DEBUG - Settings.get_story_prompt called with language={language}")
            
            if phase_prompt and "Exposition" in phase_prompt:
                previous_story_section = "This is a new story request. Create an original story based on the input."
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
                previous_story_section = "This is a new story request. Create an original story based on the input."
                continuation_instruction = "with a fresh narrative"
                story_start_instruction = "Start with a strong hook"

            prompt_config = self._load_prompt_template()
            
            # Load common config for template references
            with open("config/common_prompt.yaml", 'r') as f:
                common_config = yaml.safe_load(f)['common']
            
            def format_rule(rule, include_story_start=False):
                if isinstance(rule, str):
                    if include_story_start:
                        return rule.format(story_start_instruction=story_start_instruction)
                    return rule.format(continuation_instruction=continuation_instruction)
                elif isinstance(rule, dict):
                    key = list(rule.keys())[0]
                    value = list(rule.values())[0]
                    return f"{key}: {value}"
                return str(rule)
            
            # Format common config lists
            common_format_rules = [format_rule(rule) for rule in common_config['format_rules']]
            common_config['format_rules'] = "\n".join([f"- {rule}" for rule in common_format_rules])
            common_config['writing_style'] = "\n".join([f"- {style}" for style in common_config['writing_style']])
            common_config['language_rule'] = common_config['language_rule'].format(language=language)
            
            # Process format rules from config
            specific_format_rules = [format_rule(rule) for rule in prompt_config.get('format_rules', [])]
            format_rules = "\n".join([f"- {rule}" for rule in specific_format_rules])
            
            lexical_fields_section = "\n".join([f"- {field}" for field in chosen_lexical_fields]) if chosen_lexical_fields else "None selected"

            # Add validation for required sections
            required_sections = ['format_rules']
            for section in required_sections:
                if section not in prompt_config:
                    raise ValueError(f"Missing required prompt section: {section} in {self.DEPLOYMENT_TYPE} config")

            print("DEBUG - About to format prompt template")
            phase_endings = "\n".join([f"- {k}: {v}" for k,v in prompt_config.get('phase_endings', {}).items()])
            story_structure = "\n".join([f"- {format_rule(item, include_story_start=True)}" for item in prompt_config.get('story_structure', [])])
            genre_adaptation = "\n".join([f"- {rule}" for rule in prompt_config.get('genre_adaptation', [])])
            key_elements = "\n".join([f"- {item}" for item in prompt_config.get('key_elements', [])])
            writing_style = "\n".join([f"- {item}" for item in prompt_config.get('writing_style', [])])

            # Format TTS rules
            common_tts = common_config['tts_formatting']
            specific_tts = prompt_config.get('tts_formatting', {})
            
            tts_rules = []
            # Add common rules only once
            tts_rules.extend(common_tts['rules'])
            # Add specific rules if they exist
            if 'rules' in specific_tts:
                tts_rules.extend(specific_tts['rules'])
            
            common_config['tts_formatting'] = (
                f"Allowed punctuation: {', '.join(common_tts['allowed_punctuation'])}\n"
                + "\n".join([f"- {rule}" for rule in tts_rules])
            )

            # Format the template with both common and specific elements
            formatted_prompt = prompt_config['template'].format(
                language=language,
                user_input=user_input,
                previous_story_section=previous_story_section,
                continuation_instruction=continuation_instruction,
                story_start_instruction=story_start_instruction,
                phase_prompt=phase_prompt or "",
                format_rules=format_rules,
                lexical_fields_section=lexical_fields_section,
                phase_endings=phase_endings,
                story_structure=story_structure,
                genre_adaptation=genre_adaptation,
                key_elements=key_elements,
                writing_style=writing_style,
                common=common_config  # Pass the entire common config for template references
            )
            print("DEBUG - Successfully formatted prompt")
            return formatted_prompt
        except Exception as e:
            print(f"DEBUG - Error in Settings.get_story_prompt: {str(e)}")
            print(f"DEBUG - Error type: {type(e)}")
            raise

    class Config:
        env_file = ".env"

settings = Settings()
