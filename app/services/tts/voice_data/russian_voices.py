"""
Russian voice data for the fal.ai TTS service.
"""

RUSSIAN_VOICES = {
    "male": {
        "Andrei Conversational": "s3://voice-cloning-zero-shot/dbdd6513-2739-420c-a390-5cc82078aa67/original/manifest.json",
        "Andrei Narrative": "s3://voice-cloning-zero-shot/73083c67-097b-430c-a410-220ab0c2dea8/original/manifest.json",
        "Andrei Podcast": "s3://voice-cloning-zero-shot/2a34938c-5040-479a-9aae-08e12bc99417/original/manifest.json",
        "Efim Conversational": "s3://voice-cloning-zero-shot/63e1fb33-f44c-4f5d-9c74-598f04c2e6f2/original/manifest.json",
        "Efim Narrative": "s3://voice-cloning-zero-shot/4adb8395-2eb3-4a8a-8a0d-0a78da2b7030/original/manifest.json",
        "Efim Podcast": "s3://voice-cloning-zero-shot/32d329a9-b9d3-46b7-a62b-5a0db1c1ed7b/original/manifest.json"
    },
    "female": {}  # No female voices available yet
}

DEFAULT_RUSSIAN_VOICES = {
    "male": "Andrei Conversational",
    "female": None  # Will fall back to male voice
} 