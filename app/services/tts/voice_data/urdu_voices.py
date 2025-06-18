"""
Urdu voice data for the fal.ai TTS service.
"""

URDU_VOICES = {
    "male": {
        "Sahil Conversational": "s3://voice-cloning-zero-shot/f0e1c482-bbed-4c7e-8af0-5a9859b28f8c/original/manifest.json",
        "Sahil Narrative": "s3://voice-cloning-zero-shot/082b0195-7e30-4554-80a6-cf4a67996e8b/original/manifest.json"
    },
    "female": {}  # No female voices available yet
}

DEFAULT_URDU_VOICES = {
    "male": "Sahil Conversational",
    "female": None  # Will fall back to male voice
} 