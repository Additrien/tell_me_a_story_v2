import asyncio
import json
import os
from dotenv import load_dotenv
import fal_client

# Load environment variables from .env file
load_dotenv()

# Get API key from environment - it should already be in the format "key_id:key_secret"
FAL_API_KEY = os.getenv("FAL_API_KEY", "")
if not FAL_API_KEY:
    print("ERROR: FAL_API_KEY not found in environment variables")
    exit(1)

# Split the API key into key_id and key_secret
key_parts = FAL_API_KEY.split(":")
if len(key_parts) == 2:
    KEY_ID = key_parts[0]
    KEY_SECRET = key_parts[1]
    print(f"FAL_KEY format appears correct: [key_id]:[key_secret]")
    print(f"Key ID: {KEY_ID[:5]}...")
    print(f"Key Secret: {KEY_SECRET[:5]}...")
else:
    print(f"WARNING: FAL_KEY format is incorrect. Expected format: 'key_id:key_secret'")
    exit(1)

# Model ID for fal.ai
FAL_MODEL_ID = "fal-ai/playai/tts/dialog"

async def test_fal_api():
    # Test payload
    payload = {
        "input": "Speaker 1: This is a test message to verify the fal.ai API is working.",
        "voices": [
            {
                "voice": "s3://voice-cloning-zero-shot/09993052-0db5-4f9d-9eb4-30da05282f44/original/manifest.json",
                "turn_prefix": "Speaker 1: "
            }
        ],
        "response_format": "url"
    }
    
    print(f"Testing fal.ai API using fal-client")
    print(f"Model ID: {FAL_MODEL_ID}")
    print(f"Payload: {json.dumps(payload, indent=2)}")
    
    try:
        # Create a client with our credentials
        async_client = fal_client.AsyncClient(key_id=KEY_ID, key_secret=KEY_SECRET)
        
        # Submit the request using fal-client
        print("Submitting request...")
        handler = await async_client.submit(
            FAL_MODEL_ID,
            arguments=payload
        )
        
        print("Request submitted, waiting for events...")
        # Print events as they come in
        async for event in handler.iter_events(with_logs=True):
            print(f"Event: {event}")
        
        # Get the final result
        print("Getting final result...")
        result = await handler.get()
        print(f"Result: {json.dumps(result, indent=2)}")
        
        # If there's an audio URL, try to download it
        if "audio" in result and "url" in result["audio"]:
            audio_url = result["audio"]["url"]
            print(f"Audio URL: {audio_url}")
            print("Audio URL found in response. Test successful!")
        else:
            print(f"No audio URL found in response: {result}")
            
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    asyncio.run(test_fal_api()) 