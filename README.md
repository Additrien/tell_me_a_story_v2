# Story Teller API

This project is a FastAPI-based application that generates interactive stories for children based on voice input. It uses advanced AI models for speech recognition, story generation, and text-to-speech synthesis.

## Features
- Voice recording through microphone
- Speech-to-text transcription using Whisper
- Story generation using Gemini Pro
- Text-to-speech synthesis using Google Cloud TTS
- Support for multiple languages (English, French, Spanish, and more)
- WebSocket support for real-time story streaming
- Interactive web interface for testing

## Prerequisites

- Python 3.10 or higher
- Google Cloud account with Text-to-Speech API enabled
- Google Gemini API key
- PyAudio and its system dependencies

## Setup

1. Clone the repository:
   git clone https://github.com/Additrien/tell_me_a_story_v2
   cd tell_me_a_story_v2

2. Create a virtual environment:
   python3 -m venv venv
   source venv/bin/activate  # Linux/macOS
   # or
   .\venv\Scripts\activate  # Windows

3. Install dependencies:
   pip install -e .

   For CUDA support (optional):
   pip install -e ".[cuda]"

## Configuration

1. Create a .env file in the root directory:
   GEMINI_API_KEY=your_api_key_here
   AUDIO_DEVICE_INDEX=optional_device_index
   GOOGLE_APPLICATION_CREDENTIALS=/path/to/your/google-credentials.json
   GOOGLE_CLOUD_PROJECT=your-project-id

2. Set up Google Cloud credentials:
   - Create a service account in Google Cloud Console
   - Download the JSON credentials file
   - Set GOOGLE_APPLICATION_CREDENTIALS to point to this file

## Audio Setup

### System Dependencies

Linux (Ubuntu/Debian):
sudo apt-get update
sudo apt-get install portaudio19-dev python3-pyaudio libasound-dev

macOS:
brew install portaudio

Windows:
- PyAudio wheel should install automatically
- If not, install Visual C++ Build Tools and try again

### Audio Device Configuration

1. List available audio devices:
   python -m app.utils.list_audio_devices

2. Set the device index in your .env file:
   AUDIO_DEVICE_INDEX=your_device_index

## Running the Application

1. Start the server:
   python main.py

2. Access the web interface:
   - Open http://localhost:8000/test in your browser
   - Use the interface to record audio and generate stories

## API Endpoints

### WebSocket
- ws://localhost:8000/api/v1/ws/story/{client_id}
  - Real-time story generation and audio streaming

### REST API
- POST /api/v1/start-recording?language={lang}: Start audio recording
- POST /api/v1/stop-recording: Stop recording and process story
- GET /api/v1/stories: Get recent story history
- POST /api/v1/stories/clear: Clear story history

## Supported Languages

- English (en-US)
- French (fr-FR)
- Spanish (es-ES)
- German (de-DE)
- Italian (it-IT)
- Portuguese (pt-PT)
- Dutch (nl-NL)
- Polish (pl-PL)
- Russian (ru-RU)
- Chinese (zh-CN)
- Japanese (ja-JP)
- Korean (ko-KR)

## Development

1. Install development dependencies:
   pip install -e ".[dev]"

2. Run tests:
   pytest

## Troubleshooting

1. Audio Recording Issues:
   - Check microphone permissions
   - Verify correct audio device index
   - Ensure minimum recording length (0.5 seconds)

2. Google Cloud Issues:
   - Verify credentials file path
   - Check API enablement in Google Cloud Console
   - Ensure project has billing enabled

3. WebSocket Connection:
   - Check browser console for connection errors
   - Verify WebSocket URL matches server address
   - Ensure client ID is valid

## License

This project is licensed under the MIT License - see the LICENSE file for details.