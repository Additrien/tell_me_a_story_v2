"""
German voice data for the fal.ai TTS service.
"""

GERMAN_VOICES = {
    "female": {
        "Anke Conversational": "s3://voice-cloning-zero-shot/c1cb7f62-4a59-4593-b6c6-6b430892541d/original/manifest.json",
        "Anke Narrative": "s3://voice-cloning-zero-shot/2f91566e-215a-4234-96e2-60acf07fed5e/original/manifest.json"
    },
    "male": {
        "David Conversational": "s3://voice-cloning-zero-shot/4c8f0ddf-5c76-4ad6-ac8b-03fc96ea5233/original/manifest.json",
        "David Narrative": "s3://voice-cloning-zero-shot/84c1437e-4225-482b-bce4-d519326f9fc1/original/manifest.json",
        "Ilias Conversational": "s3://voice-cloning-zero-shot/adcf0e59-1b93-47b6-b88e-13e9c35fb6ec/original/manifest.json",
        "Ilias Narrative": "s3://voice-cloning-zero-shot/f78a1dc3-6533-4967-a0d2-88e13894a45a/original/manifest.json"
    }
}

DEFAULT_GERMAN_VOICES = {
    "female": "Anke Conversational",
    "male": "David Conversational"
} 