"""
Korean voice data for the fal.ai TTS service.
"""

KOREAN_VOICES = {
    "female": {
        "Dohee Conversational": "s3://voice-cloning-zero-shot/94c9868a-da30-4263-81f7-16c7288acd4c/original/manifest.json",
        "Dohee Narrative": "s3://voice-cloning-zero-shot/e8177169-235a-4559-a13b-baf324f96bbd/original/manifest.json"
    },
    "male": {
        "Hun Conversational": "s3://voice-cloning-zero-shot/3b32b6cd-a738-4fdc-8e29-4ef36127e6a6/original/manifest.json",
        "Hun Narrative": "s3://voice-cloning-zero-shot/f6eda8eb-ebb1-459c-a6a3-846ec588961c/original/manifest.json"
    }
}

DEFAULT_KOREAN_VOICES = {
    "female": "Dohee Conversational",
    "male": "Hun Conversational"
} 