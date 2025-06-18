"""
Hebrew voice data for the fal.ai TTS service.
"""

HEBREW_VOICES = {
    "female": {
        "Mary Conversational": "s3://voice-cloning-zero-shot/20008550-9a38-4366-93f0-76381c221fb1/original/manifest.json",
        "Mary Narrative": "s3://voice-cloning-zero-shot/08dbdaf6-8d3a-446d-8fc4-3ad69e9ee5bc/original/manifest.json",
        "Mary Podcast": "s3://voice-cloning-zero-shot/4b86ea46-2095-43a6-889c-d26146cd33d2/original/manifest.json"
    },
    "male": {}  # No male voices available yet
}

DEFAULT_HEBREW_VOICES = {
    "female": "Mary Conversational",
    "male": None  # Will fall back to female voice
} 