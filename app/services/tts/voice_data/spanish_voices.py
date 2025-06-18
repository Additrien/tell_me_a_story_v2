"""
Spanish voice data for the fal.ai TTS service.
"""

SPANISH_VOICES = {
    "male": {
        "Xavi Conversational": "s3://voice-cloning-zero-shot/b815208f-4677-4114-a0d4-64b71102c097/original/manifest.json",
        "Xavi Narrative": "s3://voice-cloning-zero-shot/36328a44-5c42-4a35-a9a1-b45596a56c88/original/manifest.json"
    },
    "female": {
        "Carmen Conversational": "s3://voice-cloning-zero-shot/3198f5d0-664c-4835-9728-92eb8cdd556c/original/manifest.json",
        "Patricia Conversational": "s3://voice-cloning-zero-shot/e0bf73c2-2b50-455a-8524-cc29de4360d1/original/manifest.json",
        "Patricia Narrative": "s3://voice-cloning-zero-shot/5694d5e5-2dfe-4440-8cc8-e2a69c3e7560/original/manifest.json",
        "Violeta Conversational": "s3://voice-cloning-zero-shot/4289181f-48fc-4c52-911f-6e769086eb98/original/manifest.json",
        "Violeta Narrative": "s3://voice-cloning-zero-shot/326c3793-b5b1-4ce3-a8ec-22c95d8553f0/original/manifest.json"
    }
}

DEFAULT_SPANISH_VOICES = {
    "male": "Xavi Conversational",
    "female": "Carmen Conversational"
} 