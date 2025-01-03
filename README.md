# Story Teller API

An AI-powered storytelling API that generates engaging stories for young children using different LLM (Language Model) providers.

## Features

- Story generation using multiple LLM providers:
  - Gemini (cloud-based)
  - Local LLaMA (runs locally)
- Multi-language support (English, French, Spanish)
- Streaming responses for real-time story generation
- Speech-to-text input support
- Text-to-speech output support
- WebSocket interface for real-time interactions

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd story-teller-api
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
.\venv\Scripts\activate  # Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file with your configuration:
```env
GEMINI_API_KEY=your_gemini_api_key
google_application_credentials=path/to/your/credentials.json
google_cloud_project=your-project-id
```

## Configuration

### LLM Service Selection

You have three ways to choose which LLM service to use, in order of priority:

1. Command-line argument (highest priority):
```bash
python main.py --llm local  # Use local LLaMA
# or
python main.py --llm gemini  # Use Gemini
```

2. Environment variable (medium priority):
```bash
export LLM_SERVICE=local  # Linux/Mac
# or
set LLM_SERVICE=local  # Windows
python main.py
```

3. Configuration file (lowest priority):
Add to your `.env` file:
```env
LLM_SERVICE=local  # or gemini
```

### Available LLM Services

1. Gemini (Default)
   - Cloud-based solution
   - Requires GEMINI_API_KEY in .env
   - Lower resource usage
   - Internet connection required

2. Local LLaMA
   - Runs completely locally
   - Higher resource usage
   - Requires GPU for optimal performance
   - No internet connection needed
   - Uses 4-bit quantization for efficient memory usage

## Usage

1. Start the server:
```bash
python main.py
```

2. The API will be available at `http://localhost:8000`

3. API Endpoints:
   - `/api/v1/story/generate` - Generate a story
   - `/api/v1/story/stream` - Stream a story in real-time
   - `/test` - WebSocket test interface

## API Documentation

Once the server is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Development

### Project Structure
```
app/
├── api/
│   ├── routes.py
│   └── websockets.py
├── core/
│   ├── config.py
│   └── languages.py
├── services/
│   ├── llm_service.py          # Base LLM interface
│   ├── gemini_llm_service.py   # Gemini implementation
│   ├── local_llm_service.py    # Local LLaMA implementation
│   ├── speech_to_text.py
│   ├── text_to_speech.py
│   └── conversation_manager.py
└── static/
    └── websocket_test.html
```

### Adding New LLM Services

1. Create a new service file in `app/services/`
2. Implement the `BaseLLMService` interface
3. Add the service to `LLMServiceFactory` in `llm_service.py`
4. Update the CLI choices and config type hints

## Requirements

- Python 3.10+
- For local LLaMA:
  - CUDA-capable GPU (recommended)
  - 8GB+ RAM
- For Gemini:
  - Internet connection
  - Valid API key

## License

MIT License

Copyright (c) 2024

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.