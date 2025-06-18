"""
Serbian voice data for the fal.ai TTS service.
"""

SERBIAN_VOICES = {
    "male": {
        "Aleksa Conversational": "s3://voice-cloning-zero-shot/3edbdafa-526e-42b9-bb74-1c66cc85edbb/original/manifest.json",
        "Aleksa Narrative": "s3://voice-cloning-zero-shot/dbe83f0d-c4d5-4ab3-8a57-6ec1f3020707/original/manifest.json",
        "Aleksa Podcast": "s3://voice-cloning-zero-shot/0b4628ea-f3cb-4935-9b47-93737fae6cae/original/manifest.json",
        "Nikola Conversational": "s3://voice-cloning-zero-shot/9d1511f0-132e-45b8-bf77-4349a81c18c5/original/manifest.json",
        "Nikola Narrative": "s3://voice-cloning-zero-shot/dd0fed8a-7b5f-45f4-97e7-e53107e0dfc1/original/manifest.json",
        "Petar Conversational": "s3://voice-cloning-zero-shot/8aae54d3-0626-4b11-be35-3a600e7eed61/original/manifest.json",
        "Petar Narrative": "s3://voice-cloning-zero-shot/f0bbd9d1-1520-42e0-8e44-e893c9613ba4/original/manifest.json",
        "Petar Podcast": "s3://voice-cloning-zero-shot/1a3ee799-1d87-46ad-8b20-2a1c6d67c60d/original/manifest.json"
    },
    "female": {
        "Dunja Conversational": "s3://voice-cloning-zero-shot/66ce2702-260a-4c29-98a9-de363485cd6d/original/manifest.json",
        "Dunja Narrative": "s3://voice-cloning-zero-shot/3bc7d453-dca0-48a8-b26b-47a6097a6ef1/original/manifest.json",
        "Dunja Podcast": "s3://voice-cloning-zero-shot/88b7b183-e5c1-4c9a-90b4-564be824cd7b/original/manifest.json",
        "Magdalena Conversational": "s3://voice-cloning-zero-shot/90bbb067-54cd-4c12-9f20-90644987cdff/original/manifest.json",
        "Magdalena Narrative": "s3://voice-cloning-zero-shot/c725b3c5-1fc0-4f64-99d5-e247203dae70/original/manifest.json",
        "Magdalena Podcast": "s3://voice-cloning-zero-shot/e778f3d0-e967-4470-9d49-68d63cb42762/original/manifest.json"
    }
}

DEFAULT_SERBIAN_VOICES = {
    "male": "Aleksa Conversational",
    "female": "Dunja Conversational"
} 