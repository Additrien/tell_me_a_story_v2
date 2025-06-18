"""
Greek voice data for the fal.ai TTS service.
"""

GREEK_VOICES = {
    "female": {
        "Bora Conversational": "s3://voice-cloning-zero-shot/7a3da4b1-5e25-4076-a368-48a9c6d2981e/original/manifest.json",
        "Bora Narrative": "s3://voice-cloning-zero-shot/f87aaa4d-6ac3-4acd-bb99-70af1ebd44b8/original/manifest.json",
        "Chrysa Conversational": "s3://voice-cloning-zero-shot/c1752411-4daa-4912-b5a0-634b25a9b63d/original/manifest.json",
        "Chrysa Narrative": "s3://voice-cloning-zero-shot/6d2b1907-f177-4fc7-8b63-d090531d17e3/original/manifest.json"
    },
    "male": {
        "Valantis Conversational": "s3://voice-cloning-zero-shot/0a314c82-0baa-4b99-a522-ea9e29e0c2f0/original/manifest.json",
        "Valantis Narrative": "s3://voice-cloning-zero-shot/0bb0d688-e738-4d1e-b777-374d1bd81e9a/original/manifest.json",
        "Valantis Podcast": "s3://voice-cloning-zero-shot/5e14b798-6c1f-46d7-925f-7562eff9f5f1/original/manifest.json"
    }
}

DEFAULT_GREEK_VOICES = {
    "female": "Bora Conversational",
    "male": "Valantis Conversational"
} 