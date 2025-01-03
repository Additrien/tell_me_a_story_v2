import torch
import os
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig, TextIteratorStreamer
from huggingface_hub import login
from threading import Thread
from typing import AsyncGenerator
from app.core.config import settings
from app.services.llm_service import BaseLLMService

class LocalLLMService(BaseLLMService):
    def __init__(self):
        # Set PyTorch memory allocator configuration
        os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "expandable_segments:True"
        
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"Initializing Llama model on {self.device}")
        
        # Enable memory efficient attention
        torch.backends.cuda.sdp_kernel(enable_flash=True, enable_math=False, enable_mem_efficient=True)
        
        # Login to Hugging Face Hub
        login(token=settings.HUGGINGFACE_TOKEN)
        
        # Configure 4-bit quantization with more aggressive memory savings
        quantization_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_compute_dtype=torch.float16,
            bnb_4bit_use_double_quant=True,
            bnb_4bit_quant_type="nf4",
            llm_int8_enable_fp32_cpu_offload=True
        )
        
        # Load model and tokenizer immediately
        self.model = AutoModelForCausalLM.from_pretrained(
            "meta-llama/Llama-3.2-1B",
            device_map="auto",
            quantization_config=quantization_config,
            torch_dtype=torch.float16,
            token=settings.HUGGINGFACE_TOKEN,
            low_cpu_mem_usage=True,
            offload_folder="offload_folder",
            max_memory={0: "1.5GiB", "cpu": "8GiB"},
            offload_state_dict=True
        )
        self.tokenizer = AutoTokenizer.from_pretrained(
            "meta-llama/Llama-3.2-1B",
            token=settings.HUGGINGFACE_TOKEN
        )
        print("Llama model initialized successfully")

    async def generate_story(self, user_input: str, language: str = "french") -> AsyncGenerator[str, None]:
        """Generate story using local Llama model"""
        try:
            prompt = self._get_story_prompt(user_input, language)
            
            inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)
            
            # Enable token streaming
            streamer = TextIteratorStreamer(self.tokenizer, skip_prompt=True)
            generation_kwargs = {
                "input_ids": inputs["input_ids"],
                "max_new_tokens": settings.LLAMA_MAX_NEW_TOKENS,
                "temperature": settings.LLAMA_TEMPERATURE,
                "top_p": settings.LLAMA_TOP_P,
                "top_k": settings.LLAMA_TOP_K,
                "streamer": streamer,
                "do_sample": True
            }

            # Start generation in a separate thread
            thread = Thread(target=self.model.generate, kwargs=generation_kwargs)
            thread.start()

            # Yield generated text chunks
            for text in streamer:
                yield text

        except Exception as e:
            print(f"Error generating story: {str(e)}")
            raise

local_llm_service = LocalLLMService() 