import aiohttp
import json
from typing import AsyncGenerator, Dict, Any
from app.core.config import settings
from app.services.llm_service import BaseLLMService

class OpenRouterError(Exception):
    def __init__(self, message: str, status_code: int = None, response_data: Dict = None):
        super().__init__(message)
        self.status_code = status_code
        self.response_data = response_data

class OpenRouterService(BaseLLMService):
    def __init__(self):
        self.model = settings.OPENROUTER_MODEL
        self.base_url = settings.OPENROUTER_BASE_URL
        self.headers = {
            "Authorization": f"Bearer {settings.OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
        }
        print(f"OpenRouterService initialized with model: {self.model}")

    async def generate_story(self, user_input: str, language: str = "french") -> AsyncGenerator[str, None]:
        """Generate a story using the OpenRouter API with streaming"""
        print(f"Starting story generation with language: {language}")
        print(f"Prompt length: {len(user_input)} characters")
        
        try:
            prompt = self._get_story_prompt(user_input, language)
            
            url = f"{self.base_url}/chat/completions"
            
            messages = [
                {"role": "system", "content": settings.get_system_prompt(language)},
                {"role": "user", "content": prompt}
            ]
            
            payload = {
                "model": self.model,
                "messages": messages,
                "stream": True,
                "temperature": settings.OPENROUTER_TEMPERATURE,
                "max_tokens": settings.OPENROUTER_MAX_TOKENS,
                "top_p": settings.OPENROUTER_TOP_P,
                "frequency_penalty": settings.OPENROUTER_FREQUENCY_PENALTY,
                "presence_penalty": settings.OPENROUTER_PRESENCE_PENALTY
            }
            
            print("Sending API request")
            
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=payload, headers=self.headers) as response:
                    if response.status != 200:
                        error_data = await response.json()
                        error_msg = error_data.get('error', {}).get('message', 'Unknown error')
                        print(f"API error: {error_msg}")
                        raise OpenRouterError(
                            f"OpenRouter API error: {error_msg}",
                            status_code=response.status,
                            response_data=error_data
                        )
                    
                    buffer = ""
                    
                    async for chunk in response.content:
                        if not chunk:
                            continue
                            
                        try:
                            chunk_text = chunk.decode('utf-8')
                            buffer += chunk_text
                            
                            while '\n' in buffer:
                                line, buffer = buffer.split('\n', 1)
                                line = line.strip()
                                
                                if not line or line.startswith(': OPENROUTER'):
                                    continue
                                
                                if line.startswith('data: '):
                                    if line == 'data: [DONE]':
                                        print("Story generation completed")
                                        break
                                    
                                    try:
                                        data = json.loads(line[6:])  # Remove 'data: ' prefix
                                        if content := data['choices'][0]['delta'].get('content'):
                                            yield content
                                    except json.JSONDecodeError as e:
                                        print(f"JSON decode error: {str(e)}")
                                        continue
                                    
                        except UnicodeDecodeError as e:
                            print(f"Unicode decode error: {str(e)}")
                            continue
                            
        except Exception as e:
            print(f"Error in story generation: {str(e)}")
            raise

openrouter_service = OpenRouterService() 