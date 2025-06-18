"""
Portuguese voice data for the fal.ai TTS service.
"""

PORTUGUESE_VOICES = {
    "male": {
        "Jorge Conversational": "s3://voice-cloning-zero-shot/063113ea-ee4e-4a25-8f79-360c29fc96c1/original/manifest.json",
        "Jorge Narrative": "s3://voice-cloning-zero-shot/ec8095bd-bbab-4229-8527-0b0ead293823/original/manifest.json",
        "Renato Conversational": "s3://voice-cloning-zero-shot/43c05226-b8f2-4e53-8184-e4beb7f4606a/original/manifest.json"
    },
    "female": {
        "Caroline Conversational": "s3://voice-cloning-zero-shot/3e27747a-b276-472c-91db-542bf88687da/original/manifest.json",
        "Caroline Narrative": "s3://voice-cloning-zero-shot/a7770c38-3246-4ddd-bf58-d8388aa42e65/original/manifest.json",
        "Jacile Conversational": "s3://voice-cloning-zero-shot/356ed0db-cb48-49fd-9a1c-922572a2be0e/original/manifest.json",
        "Jacile Narrative": "s3://voice-cloning-zero-shot/6d093315-8da6-4fd8-a4b9-5446b43ff4c7/original/manifest.json"
    }
}

DEFAULT_PORTUGUESE_VOICES = {
    "male": "Jorge Conversational",
    "female": "Caroline Conversational"
} 