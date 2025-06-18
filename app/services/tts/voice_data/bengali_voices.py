"""
Bengali voice data for the fal.ai TTS service.
"""

BENGALI_VOICES = {
    "male": {
        "Pinaki Conversational": "s3://voice-cloning-zero-shot/ef853fea-b679-4024-9733-b170a6414b6c/original/manifest.json",
        "Pinaki Narrative": "s3://voice-cloning-zero-shot/74370dcd-d229-47b1-8e82-ccc7f29d3ad5/original/manifest.json",
        "Pinaki Podcast": "s3://voice-cloning-zero-shot/e4733a9d-b57e-4770-a87f-70cd91417d83/original/manifest.json",
        "Sourav Conversational": "s3://voice-cloning-zero-shot/5a91a2b3-2a35-4147-aeb5-d0254d60c3b1/original/manifest.json",
        "Sourav Narrative": "s3://voice-cloning-zero-shot/83c50007-c32a-425c-a683-a46268c3749a/original/manifest.json"
    },
    "female": {
        "Mousmi Conversational": "s3://voice-cloning-zero-shot/1712cfb3-6774-4d2b-8ce0-f4cf94bd52d5/original/manifest.json",
        "Mousmi Narrative": "s3://voice-cloning-zero-shot/d7dfaccf-390a-488c-9a05-d100b7b8cd05/original/manifest.json",
        "Tasmia Conversational": "s3://voice-cloning-zero-shot/bf2c2226-e02c-4b8d-96ac-ff1149d95e40/original/manifest.json",
        "Tasmia Narrative": "s3://voice-cloning-zero-shot/da523c41-f801-4d60-b8aa-f0a533ef8cfa/original/manifest.json",
        "Tasmia Podcast": "s3://voice-cloning-zero-shot/c575de57-e52a-4055-bc10-19d749846dac/original/manifest.json"
    }
}

DEFAULT_BENGALI_VOICES = {
    "male": "Pinaki Conversational",
    "female": "Mousmi Conversational"
} 