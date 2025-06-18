"""
Polish voice data for the fal.ai TTS service.
"""

POLISH_VOICES = {
    "male": {
        "Adam Conversational": "s3://voice-cloning-zero-shot/294ab1d2-fdcd-4a90-9dee-b2f76676be5f/original/manifest.json",
        "Adam Narrative": "s3://voice-cloning-zero-shot/99fba53e-f238-46a7-a496-f8737197ed62/original/manifest.json",
        "Konstanty Conversational": "s3://voice-cloning-zero-shot/978eb3df-ccd3-476f-b10d-a0c4129f4956/original/manifest.json",
        "Konstanty Narrative": "s3://voice-cloning-zero-shot/0dba832f-6b03-4990-803f-f4da4852b3e6/original/manifest.json",
        "Konstanty Podcast": "s3://voice-cloning-zero-shot/d0fe1901-545a-488f-8a86-0f0d6fc6aa5b/original/manifest.json"
    },
    "female": {
        "Julia Conversational": "s3://voice-cloning-zero-shot/cad4f9fb-f47d-4beb-a668-4f348410f30c/original/manifest.json",
        "Julia Narrative": "s3://voice-cloning-zero-shot/e91f42c4-2f3a-4e62-bb7e-9e398e54b2b1/original/manifest.json",
        "Julia Podcast": "s3://voice-cloning-zero-shot/0183c952-20d6-4efa-a68e-9a2f575e2e1e/original/manifest.json"
    }
}

DEFAULT_POLISH_VOICES = {
    "male": "Adam Conversational",
    "female": "Julia Conversational"
} 