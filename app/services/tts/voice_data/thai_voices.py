"""
Thai voice data for the fal.ai TTS service.
"""

THAI_VOICES = {
    "male": {
        "Katbundit Conversational": "s3://voice-cloning-zero-shot/f80c355d-1075-4d2b-a53d-bb26aa4d1453/original/manifest.json",
        "Katbundit Narrative": "s3://voice-cloning-zero-shot/e1357526-c162-441b-afb9-285d3d21b9b4/original/manifest.json",
        "Nopparat Conversational": "s3://voice-cloning-zero-shot/59933136-5aca-4f42-827f-d354649c62a2/original/manifest.json",
        "Nopparat Narrative": "s3://voice-cloning-zero-shot/edd305a3-9cd2-4dd6-873f-9efc1f73aefc/original/manifest.json"
    },
    "female": {
        "Nattchanita Conversational": "s3://voice-cloning-zero-shot/ba9eb1c9-8897-4c41-9c79-f2cb428544a8/original/manifest.json",
        "Nattchanita Narrative": "s3://voice-cloning-zero-shot/4353be7d-8cd3-4452-9e0b-bc4078c240d7/original/manifest.json",
        "Nattha Conversational": "s3://voice-cloning-zero-shot/bb585812-1c85-4a16-90f7-09c24b6c8186/original/manifest.json",
        "Nattha Narrative": "s3://voice-cloning-zero-shot/4c495e1a-1352-4187-99eb-6e5dc7d55059/original/manifest.json"
    }
}

DEFAULT_THAI_VOICES = {
    "male": "Katbundit Conversational",
    "female": "Nattchanita Conversational"
} 