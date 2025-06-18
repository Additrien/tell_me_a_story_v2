"""
Italian voice data for the fal.ai TTS service.
"""

ITALIAN_VOICES = {
    "female": {
        "Giulia Conversational": "s3://voice-cloning-zero-shot/43ae27b5-cad2-4801-95fc-f4d53456b0ec/original/manifest.json",
        "Giulia Narrative": "s3://voice-cloning-zero-shot/1f8be5c0-848a-4de4-a32e-cdba0816a165/original/manifest.json"
    },
    "male": {
        "Alessandro Conversational": "s3://voice-cloning-zero-shot/35f48866-aae9-4bde-8264-409c4b046e74/original/manifest.json",
        "Alessandro Narrative": "s3://voice-cloning-zero-shot/4bf73a41-39f0-48a7-8c34-9b6e1720ce51/original/manifest.json",
        "Fabio Conversational": "s3://voice-cloning-zero-shot/bb24aff9-6b5f-406f-9ae2-4fff116fbb6a/original/manifest.json",
        "Fabio Narrative": "s3://voice-cloning-zero-shot/d41f196e-9dc5-461e-aa84-9d3a60f5f484/original/manifest.json",
        "Marco Conversational": "s3://voice-cloning-zero-shot/7be9afeb-40e8-4902-9af5-51f81ecd601a/original/manifest.json"
    }
}

DEFAULT_ITALIAN_VOICES = {
    "female": "Giulia Conversational",
    "male": "Alessandro Conversational"
} 