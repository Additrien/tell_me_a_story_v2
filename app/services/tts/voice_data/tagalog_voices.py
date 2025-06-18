"""
Tagalog voice data for the fal.ai TTS service.
"""

TAGALOG_VOICES = {
    "male": {
        "Aiken Conversational": "s3://voice-cloning-zero-shot/3a174cca-4ca2-4936-a0e7-e142e2f87317/original/manifest.json",
        "Aiken Narrative": "s3://voice-cloning-zero-shot/487418ee-3316-4044-afce-d18bcd3e1451/original/manifest.json",
        "Jaro Conversational": "s3://voice-cloning-zero-shot/67a8d750-e675-4ce8-856c-14a71cf15585/original/manifest.json"
    },
    "female": {}  # No female voices available yet
}

DEFAULT_TAGALOG_VOICES = {
    "male": "Aiken Conversational",
    "female": None  # Will fall back to male voice
} 