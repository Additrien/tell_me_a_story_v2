"""
Afrikaans voice data for the fal.ai TTS service.
"""

AFRIKAANS_VOICES = {
    "female": {
        "Ronel Conversational": "s3://voice-cloning-zero-shot/6c7530a7-a8dc-47d1-a854-37be19f86260/original/manifest.json",
        "Ronel Narrative": "s3://voice-cloning-zero-shot/bf646213-cb3c-447b-9d54-57f2b82298fb/original/manifest.json",
        "Ronel Podcast": "s3://voice-cloning-zero-shot/d64ed0d1-d3d1-403e-b73f-dcb7238765a4/original/manifest.json"
    },
    "male": {}  # No male voices available yet
}

DEFAULT_AFRIKAANS_VOICES = {
    "female": "Ronel Conversational",
    "male": None  # Will fall back to female voice
} 