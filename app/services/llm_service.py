import aiohttp
from app.core.config import settings
from app.services.conversation_manager import conversation_manager

async def generate_story(user_input: str, language: str = "french") -> str:
    try:
        print("USER INPUT: ", user_input)
        conversation_history = conversation_manager.get_formatted_history()
        prompt = settings.STORY_PROMPT.format(
            user_input=user_input,
            language=language,
            conversation_history=conversation_history
        )
        print("prompt: ", prompt)
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{settings.GEMINI_MODEL}:generateContent?key={settings.GEMINI_API_KEY}"
        
        async with aiohttp.ClientSession() as session:
            async with session.post(
                url,
                json={
                    "contents": [{"parts": [{"text": prompt}]}],
                    "generationConfig": {
                        "maxOutputTokens": settings.GEMINI_MAX_OUTPUT_TOKENS,
                        "temperature": settings.GEMINI_TEMPERATURE,
                        "topP": settings.GEMINI_TOP_P,
                        "topK": settings.GEMINI_TOP_K
                    }
                },
                headers={"Content-Type": "application/json"}
            ) as response:
                if response.status != 200:
                    error_text = await response.text()
                    raise Exception(f"API Error: {error_text}")
                    
                data = await response.json()
                print("LLM RESPONSE: ", data)
                story = data["candidates"][0]["content"]["parts"][0]["text"]
                conversation_manager.add_turn(user_input, story, language)
                return story
    except Exception as e:
        print(f"Error generating story: {str(e)}")
        raise
