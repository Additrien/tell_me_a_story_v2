from pydantic_settings import BaseSettings
import yaml

class Settings(BaseSettings):
    PROJECT_NAME: str = "Story Teller API"
    VERSION: str = "0.1.0"
    API_V1_STR: str = "/api/v1"
    LLM_API_KEY: str
    TTS_API_KEY: str
    WHISPER_MODEL: str = "openai/whisper-tiny"
    GEMINI_API_KEY: str
    GEMINI_MODEL: str = "gemini-1.5-flash"
    STORY_PROMPT: str = """
    You are a friendly storyteller for young children aged 6 years old. A child has just told you about something interesting. Your task is to create a short, engaging story based on what the child said. The story should:

    1. Be appropriate for a 6-year-old audience
    2. Be 3-4 sentences long
    3. Use simple language and short sentences
    4. Include a bit of magic or wonder
    5. Have a positive and uplifting tone
    6. Avoid any scary or upsetting elements

    Here's what the child said:
    "{user_input}"

    Please create a fun, imaginative story based on this input.
    """

    class Config:
        env_file = ".env"

settings = Settings()

def load_routes_config():
    with open("config/routes_config.yaml", "r") as file:
        return yaml.safe_load(file)

routes_config = load_routes_config()
