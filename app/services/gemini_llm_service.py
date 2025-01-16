import aiohttp
import json
from typing import AsyncGenerator, Optional
from app.core.config import settings
from app.services.llm_service import BaseLLMService

class GeminiLLMService(BaseLLMService):
    async def generate_story(self, user_input: str, language: str = "french", phase: Optional[str] = None, previous_content: Optional[str] = None) -> AsyncGenerator[str, None]:
        try:
            prompt = self._get_story_prompt(user_input, language, phase, previous_content)
            
            # Adjust max tokens based on phase if applicable
            max_tokens = settings.STORY_PHASES[phase]["max_tokens"] if phase and settings.ENABLE_PHASED_GENERATION else settings.GEMINI_MAX_OUTPUT_TOKENS
            
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{settings.GEMINI_MODEL}:streamGenerateContent?alt=sse&key={settings.GEMINI_API_KEY}"
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    url,
                    json={
                        "contents": [{"parts": [{"text": prompt}]}],
                        "generationConfig": {
                            "maxOutputTokens": max_tokens,
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