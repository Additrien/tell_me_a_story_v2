"""
Japanese voice data for the fal.ai TTS service.
"""

JAPANESE_VOICES = {
    "female": {
        "Kiriko Conversational": "s3://voice-cloning-zero-shot/f5dee056-a6fe-488f-99d7-5a7d30823c31/original/manifest.json",
        "Kiriko Narrative": "s3://voice-cloning-zero-shot/63cdb0d7-cc74-4894-97b8-60337507707e/original/manifest.json",
        "Yumiko Conversatioanl": "s3://voice-cloning-zero-shot/3139176d-c6c1-4c74-9774-29239062ec3b/original/manifest.json",
        "Yumiko Narrative": "s3://voice-cloning-zero-shot/627b1059-0ae7-4dd8-a494-d36c8f143b0a/original/manifest.json"
    },
    "male": {
        "Koji Conversational": "s3://voice-cloning-zero-shot/cf813b9f-4da6-4586-906f-b07842a17601/original/manifest.json",
        "Koji Narrative": "s3://voice-cloning-zero-shot/5ff94985-a335-4093-b3c0-0b4ffac5d5fc/original/manifest.json",
        "Jun Conversational": "s3://voice-cloning-zero-shot/00325021-7969-4c8b-949f-0b6cbb043ea2/original/manifest.json",
        "Jun Narrative": "s3://voice-cloning-zero-shot/a0d2104c-40aa-4d7a-8eb6-6d8c937e0d38/original/manifest.json",
        "Tsukasa Conversational": "s3://voice-cloning-zero-shot/c4ee9511-d053-4720-8813-c0844402d5ce/original/manifest.json",
        "Tsukasa Narrative": "s3://voice-cloning-zero-shot/22de0371-a2f5-4495-a5bd-509ae5e31c78/original/manifest.json"
    }
}

DEFAULT_JAPANESE_VOICES = {
    "female": "Kiriko Conversational",
    "male": "Koji Conversational"
} 