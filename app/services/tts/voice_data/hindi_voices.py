"""
Hindi voice data for the fal.ai TTS service.
"""

HINDI_VOICES = {
    "female": {
        "Maanekshi Conversational": "s3://voice-cloning-zero-shot/8049484f-3055-42b8-ab13-25ccf0475710/original/manifest.json",
        "Maanekshi Narrative": "s3://voice-cloning-zero-shot/bc3aac42-8e8f-43e2-8919-540f817a0ac4/original/manifest.json",
        "Neeti Conversational": "s3://voice-cloning-zero-shot/6089034b-bda6-4a76-a9e1-709b3a881514/original/manifest.json",
        "Neeti Narrative": "s3://voice-cloning-zero-shot/b81c4ecc-b74f-4482-bd6c-026adbb84c76/original/manifest.json"
    },
    "male": {
        "Anuj Conversational": "s3://voice-cloning-zero-shot/6f3decaf-f64f-414a-b16a-f8a1492d28a6/original/manifest.json",
        "Anuj Narrative": "s3://voice-cloning-zero-shot/610e98bb-5c9c-4a98-b390-94d539a77996/original/manifest.json",
        "Pravin Conversational": "s3://voice-cloning-zero-shot/e4749094-943d-4751-82e0-c13930e0a659/original/manifest.json",
        "Pravin Narrative": "s3://voice-cloning-zero-shot/13ff8c72-7e5a-471e-b3fc-0e708ea4046c/original/manifest.json",
        "Sachin Conversational": "s3://voice-cloning-zero-shot/29c3fc22-d566-492c-b38a-5797862dc1ee/original/manifest.json",
        "Sachin Narrative": "s3://voice-cloning-zero-shot/f0c4da39-8030-474b-ae88-e76312b98ae1/original/manifest.json"
    }
}

DEFAULT_HINDI_VOICES = {
    "female": "Neeti Conversational",
    "male": "Anuj Conversational"
} 