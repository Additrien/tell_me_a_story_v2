# Story Teller API

This project is a FastAPI-based application that generates stories for children based on voice input.

## Features
- Voice recording through microphone
- Speech-to-text transcription using Whisper
- Story generation using Gemini Pro
- Text-to-speech synthesis using MMS-TTS
- Support for multiple languages

## Setup

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/story_teller_api.git
   cd story_teller_api
   ```

2. Create a virtual environment:
   ```
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:
   ```
   pip install -e .
   ```

## Audio Setup

### PyAudio Installation
PyAudio requires system-level dependencies. Install them before proceeding:

#### Linux (Ubuntu/Debian):
```
sudo apt-get update
sudo apt-get install portaudio19-dev python3-pyaudio libasound-dev
```

#### macOS:
```
brew install portaudio
```

### Audio Device Configuration
1. List available audio devices:
```
python -m app.utils.list_audio_devices
```

2. Configure input device (optional):
   - Note the device index from the list
   - Set `AUDIO_DEVICE_INDEX` in your environment variables or `.env` file

### Troubleshooting Audio Issues

If you encounter audio input/output issues:

1. Check device permissions:
   - Ensure your user has access to audio devices
   - For Linux: Add user to audio group: `sudo usermod -a -G audio $USER`

2. Test recording:
   ```bash
   curl -X POST "http://localhost:8000/api/v1/start-recording?language=english"
   # Speak into microphone
   curl -X POST "http://localhost:8000/api/v1/stop-recording"
   ```

3. Common Issues:
   - "No working input device found": Check microphone connections and permissions
   - "Recording too short": Ensure minimum 0.5 seconds of audio
   - ALSA errors: Can be safely ignored (redirected to /dev/null)

## Environment Variables

Create a `.env` file in the root directory with the following variables:

```
GEMINI_API_KEY=your_api_key_here
AUDIO_DEVICE_INDEX=optional_device_index
```

## Running the Application

1. Start the server:
```
python main.py
```

2. The API will be available at `http://localhost:8000`

## API Endpoints

- `POST /api/v1/start-recording`: Start audio recording
- `POST /api/v1/stop-recording`: Stop recording and process story
- `POST /api/v1/transcribe`: Convert audio to text
- `POST /api/v1/generate-story`: Generate story from text
- `POST /api/v1/text-to-speech`: Convert story to speech
- `POST /api/v1/full-process`: Complete pipeline from audio to story

## Supported Languages

The application supports multiple languages including:
- English
- French
- Spanish
- German
- Italian
- Portuguese
- Dutch
- Polish
- Russian
- Chinese
- Japanese
- Korean

## Development

1. Install development dependencies:
```
pip install -e ".[dev]"
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.