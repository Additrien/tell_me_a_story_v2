"""
French voice data for the fal.ai TTS service.
"""

FRENCH_VOICES = {
    "female": {
        "Ange Conversational": "s3://voice-cloning-zero-shot/09993052-0db5-4f9d-9eb4-30da05282f44/original/manifest.json",
        "Ange Narrative": "s3://voice-cloning-zero-shot/067f8a04-9138-440b-971d-5cce69f4c271/original/manifest.json",
        "Gaelle Conversational": "s3://voice-cloning-zero-shot/7101ecc1-8071-47c8-a7d2-ffef2000616c/original/manifest.json",
        "Gaelle Narrative": "s3://voice-cloning-zero-shot/19561064-851a-4740-95fa-34d4bf16fa4f/original/manifest.json"
    },
    "male": {
        "Laurence Conversational": "s3://voice-cloning-zero-shot/94453b23-b60c-4852-9eac-ae76166b1ba5/original/manifest.json",
        "Laurence Narrative": "s3://voice-cloning-zero-shot/21ca9f6f-6044-489a-a901-18867690622c/original/manifest.json"
    }
}

DEFAULT_FRENCH_VOICES = {
    "female": "Ange Conversational",
    "male": "Laurence Conversational"
} 