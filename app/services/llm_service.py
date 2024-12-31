import aiohttp
import json
from typing import AsyncGenerator
from app.core.config import settings

async def generate_story(user_input: str, language: str = "french", add_to_history: bool = True) -> AsyncGenerator[str, None]:
    try:
        print("USER INPUT: ", user_input)
        prompt = settings.STORY_PROMPT.format(
            user_input=user_input,
            language=language
        )
        print("prompt: ", prompt)
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{settings.GEMINI_MODEL}:streamGenerateContent?alt=sse&key={settings.GEMINI_API_KEY}"
        
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
                
                async for line in response.content:
                    if line:
                        chunk = line.decode('utf-8').strip()
                        if chunk.startswith('data: '):
                            try:
                                data = json.loads(chunk[6:])  # Remove 'data: ' prefix
                                if 'candidates' in data and data['candidates']:
                                    text = data['candidates'][0]['content']['parts'][0]['text']
                                    yield text
                            except json.JSONDecodeError:
                                if chunk != 'data: [DONE]':  # Ignore end marker
                                    print(f"Failed to parse chunk: {chunk}")
                                continue
                
    except Exception as e:
        print(f"Error generating story: {str(e)}")
        raise
