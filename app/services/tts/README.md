# Text-to-Speech (TTS) Service

This directory contains the implementation of the Text-to-Speech service used in the Story Teller application.

## Overview

The TTS service is responsible for converting text to speech audio. It currently uses the fal.ai API for high-quality voice synthesis.

## Voice System

The voice system is organized as follows:

1. **FalTTSService**: The main service class that handles API communication with fal.ai.
2. **Voice Data**: Voice IDs are organized by language and gender in separate files under `voice_data/`.

### Available Languages

The system currently supports the following languages:

- English (US) - `en-US` - 60+ voices (15+ male, 7+ female, 40+ neutral)
- Arabic - `ar-AR` - 8 voices (4 male, 4 female)
- Bengali - `bn-BN` - 10 voices (5 male, 5 female)
- Portuguese - `pt-PT` - 7 voices (3 male, 4 female)
- Afrikaans - `af-ZA` - 3 voices (0 male, 3 female)
- French - `fr-FR` - 6 voices (2 male, 4 female)
- German - `de-DE` - 6 voices (4 male, 2 female)
- Greek - `el-GR` - 7 voices (3 male, 4 female)
- Hindi - `hi-IN` - 10 voices (6 male, 4 female)
- Italian - `it-IT` - 7 voices (5 male, 2 female)
- Japanese - `ja-JP` - 10 voices (6 male, 4 female)
- Korean - `ko-KR` - 4 voices (2 male, 2 female)
- Malay - `ms-MY` - 3 voices (3 male, 0 female)
- Russian - `ru-RU` - 6 voices (6 male, 0 female)
- Polish - `pl-PL` - 8 voices (5 male, 3 female)
- Serbian - `sr-RS` - 14 voices (8 male, 6 female)
- Spanish - `es-ES` - 7 voices (2 male, 5 female)
- Tagalog - `tl-PH` - 3 voices (3 male, 0 female)
- Thai - `th-TH` - 8 voices (4 male, 4 female)
- Turkish - `tr-TR` - 3 voices (3 male, 0 female)
- Urdu - `ur-PK` - 2 voices (2 male, 0 female)
- Hebrew - `he-IL` - 3 voices (0 male, 3 female)
- Dutch - `nl-NL` - 0 voices (falls back to English)
- Chinese - `zh-CN` - 0 voices (falls back to English)

### Voice Organization

Voices are organized in separate files by language:
- `english_us_voices.py` - English US voices
- `arabic_voices.py` - Arabic voices
- `bengali_voices.py` - Bengali voices
- `portuguese_voices.py` - Portuguese voices
- `afrikaans_voices.py` - Afrikaans voices
- `french_voices.py` - French voices
- `german_voices.py` - German voices
- `greek_voices.py` - Greek voices
- `hindi_voices.py` - Hindi voices
- `italian_voices.py` - Italian voices
- `japanese_voices.py` - Japanese voices
- `korean_voices.py` - Korean voices
- `malay_voices.py` - Malay voices
- `russian_voices.py` - Russian voices
- `polish_voices.py` - Polish voices
- `serbian_voices.py` - Serbian voices
- `spanish_voices.py` - Spanish voices
- `tagalog_voices.py` - Tagalog voices
- `thai_voices.py` - Thai voices
- `turkish_voices.py` - Turkish voices
- `urdu_voices.py` - Urdu voices
- `hebrew_voices.py` - Hebrew voices
- `dutch_voices.py` - Dutch voices (placeholder)
- `chinese_voices.py` - Chinese voices (placeholder)

Each file defines:
1. A dictionary of voices by gender
2. Default voices for each gender

### Voice Selection

Voices are selected based on:
1. The language of the text
2. The requested gender (male, female, or neutral)

If a specific language or gender is not available, the system will fall back to:
1. Another gender in the same language
2. English (US) as the ultimate fallback

### Default Voices

Each language has default voices for each gender. Here are some examples:

- English (US):
  - Male: "Dexter"
  - Female: "Jennifer"
  - Neutral: "Alex"

- Arabic:
  - Male: "Abdo Conversational"
  - Female: "Maryem Conversational"

- French:
  - Male: "Laurence Conversational"
  - Female: "Ange Conversational"

- German:
  - Male: "David Conversational"
  - Female: "Anke Conversational"

- Japanese:
  - Male: "Koji Conversational"
  - Female: "Kiriko Conversational"
  
- Spanish:
  - Male: "Xavi Conversational"
  - Female: "Carmen Conversational"
  
- Thai:
  - Male: "Katbundit Conversational"
  - Female: "Nattchanita Conversational"
  
- Serbian:
  - Male: "Aleksa Conversational"
  - Female: "Dunja Conversational"

## Adding New Voices

To add new voices:

1. Create a new file in `voice_data/` for the language if it doesn't exist (e.g., `chinese_voices.py`)
2. Add the voice data in the format:
   ```python
   LANGUAGE_VOICES = {
       "male": {
           "Voice Name": "voice_id",
           ...
       },
       "female": {
           "Voice Name": "voice_id",
           ...
       }
   }
   
   DEFAULT_LANGUAGE_VOICES = {
       "male": "Default Male Voice Name",
       "female": "Default Female Voice Name"
   }
   ```
3. Import and add the new voice data in `voice_data/__init__.py`:
   ```python
   from app.services.tts.voice_data.chinese_voices import CHINESE_VOICES, DEFAULT_CHINESE_VOICES
   
   # Add to VOICE_DATA dictionary
   VOICE_DATA = {
       # Existing languages...
       "zh-CN": CHINESE_VOICES,
   }
   
   # Add to DEFAULT_VOICES dictionary
   DEFAULT_VOICES = {
       # Existing languages...
       "zh-CN": DEFAULT_CHINESE_VOICES,
   }
   ```

## Configuration

The TTS service requires an API key from fal.ai. Set this in your `.env` file:

```
FAL_API_KEY=your_api_key_here
```

## Usage

The TTS service is used through the `TTSFactory`:

```python
from app.services.tts.tts_factory import tts_factory

# Get the default TTS service
tts_service = tts_factory.get_service()

# Convert text to speech
audio_bytes = await tts_service.convert_text_to_speech(
    text="Hello, world!",
    story_id="story_123",
    language="english",
    gender="female"
)
``` 