"""
Arabic voice data for the fal.ai TTS service.
"""

ARABIC_VOICES = {
    "male": {
        "Abdo Conversational": "s3://voice-cloning-zero-shot/181231d7-b84e-4845-86bf-1a61bf8784e6/original/manifest.json",
        "Abdo Narrative": "s3://voice-cloning-zero-shot/412c739c-d89e-4402-ac2c-7c107606bcf8/original/manifest.json",
        "Ahmed Conversational": "s3://voice-cloning-zero-shot/6045da2d-8cb1-49b8-ac3a-cd5ddd745506/original/manifest.json",
        "Ahmed Narrative": "s3://voice-cloning-zero-shot/c8731d9b-c16c-4dda-b320-7db983806687/original/manifest.json"
    },
    "female": {
        "Maryem Conversational": "s3://voice-cloning-zero-shot/d44b758a-f3e7-4a7c-af50-02451c7101f4/original/manifest.json",
        "Maryem Narrative": "s3://voice-cloning-zero-shot/b6f988dc-c137-4753-ad11-aa7cb021e17/original/manifest.json",
        "Shrouk Conversational": "s3://voice-cloning-zero-shot/67c03807-03c3-496b-bcb4-aebd3afa2497/original/manifest.json",
        "Shrouk Narrative": "s3://voice-cloning-zero-shot/4aa345f0-768b-43d8-86c7-10006f73e377/original/manifest.json"
    }
}

DEFAULT_ARABIC_VOICES = {
    "male": "Abdo Conversational",
    "female": "Maryem Conversational"
} 