"""
Voice data for the fal.ai TTS service.
"""

from app.services.tts.voice_data.arabic_voices import ARABIC_VOICES, DEFAULT_ARABIC_VOICES
from app.services.tts.voice_data.bengali_voices import BENGALI_VOICES, DEFAULT_BENGALI_VOICES
from app.services.tts.voice_data.portuguese_voices import PORTUGUESE_VOICES, DEFAULT_PORTUGUESE_VOICES
from app.services.tts.voice_data.english_us_voices import ENGLISH_US_VOICES, DEFAULT_ENGLISH_US_VOICES
from app.services.tts.voice_data.afrikaans_voices import AFRIKAANS_VOICES, DEFAULT_AFRIKAANS_VOICES
from app.services.tts.voice_data.french_voices import FRENCH_VOICES, DEFAULT_FRENCH_VOICES
from app.services.tts.voice_data.german_voices import GERMAN_VOICES, DEFAULT_GERMAN_VOICES
from app.services.tts.voice_data.greek_voices import GREEK_VOICES, DEFAULT_GREEK_VOICES
from app.services.tts.voice_data.hindi_voices import HINDI_VOICES, DEFAULT_HINDI_VOICES
from app.services.tts.voice_data.italian_voices import ITALIAN_VOICES, DEFAULT_ITALIAN_VOICES
from app.services.tts.voice_data.japanese_voices import JAPANESE_VOICES, DEFAULT_JAPANESE_VOICES
from app.services.tts.voice_data.korean_voices import KOREAN_VOICES, DEFAULT_KOREAN_VOICES
from app.services.tts.voice_data.malay_voices import MALAY_VOICES, DEFAULT_MALAY_VOICES
from app.services.tts.voice_data.russian_voices import RUSSIAN_VOICES, DEFAULT_RUSSIAN_VOICES
from app.services.tts.voice_data.polish_voices import POLISH_VOICES, DEFAULT_POLISH_VOICES
from app.services.tts.voice_data.serbian_voices import SERBIAN_VOICES, DEFAULT_SERBIAN_VOICES
from app.services.tts.voice_data.spanish_voices import SPANISH_VOICES, DEFAULT_SPANISH_VOICES
from app.services.tts.voice_data.tagalog_voices import TAGALOG_VOICES, DEFAULT_TAGALOG_VOICES
from app.services.tts.voice_data.thai_voices import THAI_VOICES, DEFAULT_THAI_VOICES
from app.services.tts.voice_data.turkish_voices import TURKISH_VOICES, DEFAULT_TURKISH_VOICES
from app.services.tts.voice_data.urdu_voices import URDU_VOICES, DEFAULT_URDU_VOICES
from app.services.tts.voice_data.hebrew_voices import HEBREW_VOICES, DEFAULT_HEBREW_VOICES
from app.services.tts.voice_data.dutch_voices import DUTCH_VOICES, DEFAULT_DUTCH_VOICES
from app.services.tts.voice_data.chinese_voices import CHINESE_VOICES, DEFAULT_CHINESE_VOICES

# Mapping of language codes to voice data
VOICE_DATA = {
    "en-US": ENGLISH_US_VOICES,
    "ar-AR": ARABIC_VOICES,
    "bn-BN": BENGALI_VOICES,
    "pt-PT": PORTUGUESE_VOICES,
    "af-ZA": AFRIKAANS_VOICES,
    "fr-FR": FRENCH_VOICES,
    "de-DE": GERMAN_VOICES,
    "el-GR": GREEK_VOICES,
    "hi-IN": HINDI_VOICES,
    "it-IT": ITALIAN_VOICES,
    "ja-JP": JAPANESE_VOICES,
    "ko-KR": KOREAN_VOICES,
    "ms-MY": MALAY_VOICES,
    "ru-RU": RUSSIAN_VOICES,
    "pl-PL": POLISH_VOICES,
    "sr-RS": SERBIAN_VOICES,
    "es-ES": SPANISH_VOICES,
    "tl-PH": TAGALOG_VOICES,
    "th-TH": THAI_VOICES,
    "tr-TR": TURKISH_VOICES,
    "ur-PK": URDU_VOICES,
    "he-IL": HEBREW_VOICES,
    "nl-NL": DUTCH_VOICES,
    "zh-CN": CHINESE_VOICES
}

# Default voices for each language
DEFAULT_VOICES = {
    "en-US": DEFAULT_ENGLISH_US_VOICES,
    "ar-AR": DEFAULT_ARABIC_VOICES,
    "bn-BN": DEFAULT_BENGALI_VOICES,
    "pt-PT": DEFAULT_PORTUGUESE_VOICES,
    "af-ZA": DEFAULT_AFRIKAANS_VOICES,
    "fr-FR": DEFAULT_FRENCH_VOICES,
    "de-DE": DEFAULT_GERMAN_VOICES,
    "el-GR": DEFAULT_GREEK_VOICES,
    "hi-IN": DEFAULT_HINDI_VOICES,
    "it-IT": DEFAULT_ITALIAN_VOICES,
    "ja-JP": DEFAULT_JAPANESE_VOICES,
    "ko-KR": DEFAULT_KOREAN_VOICES,
    "ms-MY": DEFAULT_MALAY_VOICES,
    "ru-RU": DEFAULT_RUSSIAN_VOICES,
    "pl-PL": DEFAULT_POLISH_VOICES,
    "sr-RS": DEFAULT_SERBIAN_VOICES,
    "es-ES": DEFAULT_SPANISH_VOICES,
    "tl-PH": DEFAULT_TAGALOG_VOICES,
    "th-TH": DEFAULT_THAI_VOICES,
    "tr-TR": DEFAULT_TURKISH_VOICES,
    "ur-PK": DEFAULT_URDU_VOICES,
    "he-IL": DEFAULT_HEBREW_VOICES,
    "nl-NL": DEFAULT_DUTCH_VOICES,
    "zh-CN": DEFAULT_CHINESE_VOICES
} 