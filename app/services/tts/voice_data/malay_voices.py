"""
Malay voice data for the fal.ai TTS service.
"""

MALAY_VOICES = {
    "male": {
        "Ignatius Conversational": "s3://voice-cloning-zero-shot/b611926f-9c79-49a6-ad7b-cc810ed80186/original/manifest.json",
        "Ignatius Narrative": "s3://voice-cloning-zero-shot/2ccd3db8-8544-49e6-824f-ae67c9b99a62/original/manifest.json",
        "Ignatius Podcast": "s3://voice-cloning-zero-shot/0d037121-dccb-4f32-bdf4-ef9c94c8ec7f/original/manifest.json"
    },
    "female": {}  # No female voices available yet
}

DEFAULT_MALAY_VOICES = {
    "male": "Ignatius Conversational",
    "female": None  # Will fall back to male voice
} 