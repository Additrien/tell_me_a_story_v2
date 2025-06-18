"""
Turkish voice data for the fal.ai TTS service.
"""

TURKISH_VOICES = {
    "male": {
        "Ali Conversational": "s3://voice-cloning-zero-shot/39ca9ea3-e576-43c7-b06e-9574b410e8e9/original/manifest.json",
        "Ali Narrative": "s3://voice-cloning-zero-shot/832368bb-16b1-4835-888d-a4826b25ab24/original/manifest.json",
        "Ali Podcast": "s3://voice-cloning-zero-shot/7b81e974-1518-4f7c-8f44-20c491ef2161/original/manifest.json"
    },
    "female": {}  # No female voices available yet
}

DEFAULT_TURKISH_VOICES = {
    "male": "Ali Conversational",
    "female": None  # Will fall back to male voice
} 