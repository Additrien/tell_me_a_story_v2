# Story Teller API

This project is a FastAPI-based application that generates stories for children based on voice input.

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
   pip install -r requirements.txt
   ```

## PyAudio Installation Issues

If you encounter issues installing PyAudio, follow these steps:

1. Install system dependencies:
   ```
   sudo apt-get update
   sudo apt-get install portaudio19-dev python3-dev
   ```

2. If you're still facing issues, try installing additional audio-related libraries:
   ```
   sudo apt-get install libasound-dev
   ```

3. After installing these dependencies, recreate your virtual environment:
   ```
   deactivate
   rm -rf venv
   python3 -m venv venv
   source venv/bin/activate
   ```

4. Reinstall the requirements:
   ```
   pip install -r requirements.txt
   ```

If you continue to face issues, you can try installing PyAudio using the system package manager:
