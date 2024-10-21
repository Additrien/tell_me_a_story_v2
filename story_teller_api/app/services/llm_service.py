import google.generativeai as genai
from app.core.config import settings

genai.configure(api_key=settings.GEMINI_API_KEY)

async def generate_story(user_input: str) -> str:
    model = genai.GenerativeModel(settings.GEMINI_MODEL)
    prompt = settings.STORY_PROMPT.format(user_input=user_input)

    response = await model.generate_content(prompt)
    return response.text
