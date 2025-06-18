import aiohttp
import json
import traceback
from typing import AsyncGenerator, Optional, List
from app.core.config import settings
from app.services.llm.base import BaseLLMService

class GeminiLLMService(BaseLLMService):
    async def generate_story(
        self, 
        user_input: str, 
        language: str = "french", 
        phase: Optional[str] = None, 
        previous_content: Optional[str] = None,
        chosen_lexical_fields: Optional[List[str]] = None
    ) -> AsyncGenerator[str, None]:
        try:
            print(f"\n=== Gemini API Request ===")
            print(f"User input: {user_input[:100]}{'...' if len(user_input) > 100 else ''}")
            print(f"Language: {language}")
            print(f"Phase: {phase}")
            print(f"Lexical fields: {chosen_lexical_fields}")
            
            prompt = self._get_story_prompt(user_input, language, phase, previous_content, chosen_lexical_fields)
            print(f"Prompt length: {len(prompt)} characters")
            
            # Adjust max tokens based on phase if applicable
            max_tokens = settings.STORY_PHASES[phase]["max_tokens"] if phase and settings.ENABLE_PHASED_GENERATION else settings.GEMINI_MAX_OUTPUT_TOKENS
            print(f"Max tokens: {max_tokens}")
            
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{settings.GEMINI_MODEL}:streamGenerateContent?alt=sse&key={settings.GEMINI_API_KEY}"
            
            request_data = {
                "contents": [{"parts": [{"text": prompt}]}],
                "generationConfig": {
                    "maxOutputTokens": max_tokens,
                    "temperature": settings.GEMINI_TEMPERATURE,
                    "topP": settings.GEMINI_TOP_P,
                    "topK": settings.GEMINI_TOP_K
                }
            }
            print(f"Request config: temperature={settings.GEMINI_TEMPERATURE}, topP={settings.GEMINI_TOP_P}, topK={settings.GEMINI_TOP_K}")
            
            async with aiohttp.ClientSession() as session:
                print(f"Sending request to Gemini API...")
                async with session.post(
                    url,
                    json=request_data,
                    headers={"Content-Type": "application/json"}
                ) as response:
                    print(f"Gemini API response status: {response.status}")
                    if response.status != 200:
                        error_text = await response.text()
                        print(f"API Error response: {error_text}")
                        raise Exception(f"API Error: {error_text}")
                    
                    print(f"Starting to process Gemini API response stream...")
                    chunk_count = 0
                    total_text_length = 0
                    
                    async for line in response.content:
                        if line:
                            chunk = line.decode('utf-8').strip()
                            if chunk.startswith('data: '):
                                try:
                                    if chunk == 'data: [DONE]':
                                        print(f"Received stream end marker")
                                        continue
                                        
                                    data = json.loads(chunk[6:])  # Remove 'data: ' prefix
                                    if 'candidates' in data and data['candidates']:
                                        text = data['candidates'][0]['content']['parts'][0]['text']
                                        chunk_count += 1
                                        total_text_length += len(text)
                                        if chunk_count % 10 == 0:  # Log every 10 chunks to avoid excessive logging
                                            print(f"Received chunk #{chunk_count}, total text length: {total_text_length}")
                                        yield text
                                except json.JSONDecodeError:
                                    print(f"Failed to parse chunk: {chunk}")
                                    continue
                                except Exception as chunk_error:
                                    print(f"Error processing chunk: {str(chunk_error)}")
                                    print(f"Problematic chunk: {chunk}")
                                    print(traceback.format_exc())
                                    continue
                    
                    print(f"Completed Gemini API response processing. Total chunks: {chunk_count}, total text length: {total_text_length}")
                    
        except Exception as e:
            print(f"Error generating story: {str(e)}")
            print(traceback.format_exc())
            raise 