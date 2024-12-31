"""Language configuration and mapping utilities."""

# Simple language names to ISO codes (for speech-to-text)
LANGUAGE_TO_ISO = {
    "french": "fr",
    "english": "en",
    "spanish": "es",
    "german": "de",
    "italian": "it",
    "portuguese": "pt",
    "dutch": "nl",
    "polish": "pl",
    "russian": "ru",
    "chinese": "zh",
    "japanese": "ja",
    "korean": "ko"
}

# Simple language names to BCP-47 codes (for text-to-speech)
LANGUAGE_TO_BCP47 = {
    "french": "fr-FR",
    "english": "en-US",
    "spanish": "es-ES",
    "german": "de-DE",
    "italian": "it-IT",
    "portuguese": "pt-PT",
    "dutch": "nl-NL",
    "polish": "pl-PL",
    "russian": "ru-RU",
    "chinese": "zh-CN",
    "japanese": "ja-JP",
    "korean": "ko-KR"
}

# Voice mappings for each supported BCP-47 language
TTS_VOICES = {
    "fr-FR": "fr-FR-Studio-D",
    "en-US": "en-US-Studio-M",
    "es-ES": "es-ES-Studio-B",
    "de-DE": "de-DE-Studio-B",
    "it-IT": "it-IT-Studio-B",
    "pt-PT": "pt-PT-Studio-B",
    "nl-NL": "nl-NL-Standard-B",
    "pl-PL": "pl-PL-Standard-B",
    "ru-RU": "ru-RU-Standard-B",
    "zh-CN": "zh-CN-Standard-B",
    "ja-JP": "ja-JP-Standard-B",
    "ko-KR": "ko-KR-Standard-B"
}

DEFAULT_LANGUAGE = "french"
DEFAULT_BCP47 = LANGUAGE_TO_BCP47[DEFAULT_LANGUAGE] 