from setuptools import setup, find_packages
import os
import subprocess
import sys
import shutil
from pathlib import Path

def is_command_available(command):
    """Check if a command is available in PATH"""
    return shutil.which(command) is not None

def install_system_dependencies():
    """Install and check required system dependencies"""
    # Function to run apt commands with sudo
    def run_apt_command(command):
        try:
            subprocess.run(["sudo", "apt-get"] + command, check=True)
            return True
        except subprocess.CalledProcessError:
            return False
    
    # Update package list
    print("Updating package list...")
    run_apt_command(["update"])
    
    # Install git-lfs if not present
    if not is_command_available("git-lfs"):
        print("Installing git-lfs...")
        if not run_apt_command(["install", "-y", "git-lfs"]):
            print("ERROR: Failed to install git-lfs")
            sys.exit(1)
    else:
        print("git-lfs is already installed")
    
    # Install espeak-ng if not present
    if not is_command_available("espeak-ng"):
        print("Installing espeak-ng...")
        if not run_apt_command(["install", "-y", "espeak-ng"]):
            print("ERROR: Failed to install espeak-ng")
            sys.exit(1)
    else:
        print("espeak-ng is already installed")

def download_tts_model():
    """Download the Kokoro TTS model if not already present"""
    model_dir = Path("app/models/kokoro")
    
    if not model_dir.exists():
        print("Downloading Kokoro TTS model...")
        model_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize git-lfs BEFORE cloning
        try:
            subprocess.run(["git", "lfs", "install"], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error initializing git-lfs: {e}")
            sys.exit(1)
        
        # Clone the model repository
        try:
            subprocess.run([
                "git", "clone",
                "https://huggingface.co/hexgrad/Kokoro-82M",
                str(model_dir)
            ], check=True)
            print("Kokoro TTS model downloaded successfully")
        except subprocess.CalledProcessError as e:
            print(f"Error cloning Kokoro model: {e}")
            print("Make sure you have git-lfs installed and authentication is set up correctly.")
            sys.exit(1)
    else:
        print("Kokoro TTS model already exists")
    
    # Create required directories
    Path("debug/audio").mkdir(parents=True, exist_ok=True)
    Path("output/audio").mkdir(parents=True, exist_ok=True)

if __name__ == "__main__":
    # Install system dependencies
    install_system_dependencies()
    
    # Download TTS model during setup
    download_tts_model()

setup(
    name="tell_me_a_story",
    version="0.1.0",
    packages=find_packages(include=['app*', 'models*']),
    install_requires=[
        # Core dependencies
        "fastapi==0.115.2",
        "uvicorn==0.32.0",
        "python-multipart==0.0.12",
        "pydantic-settings==2.6.0",
        "pyyaml==6.0.2",
        
        # Google Cloud
        "google-cloud-texttospeech>=2.15.0",
        "google-cloud-core>=2.3.3",
        "google-api-core>=2.15.0",
        "google-auth>=2.27.0",
        
        # Audio processing
        "pyaudio==0.2.14",
        "soundfile==0.12.1",
        "librosa==0.9.1",
        "SpeechRecognition==3.11.0",
        "sounddevice>=0.4.6",
        
        # HTTP client
        "aiohttp==3.11.11",
        "aiofiles>=23.2.1",
        
        # ML dependencies
        "numpy>=1.24.3",
        "transformers>=4.38.0",
        "datasets>=2.18.0",
        "huggingface-hub>=0.19.0",
        "torchaudio>=2.0.0",
        "bitsandbytes==0.45.0",
        "accelerate>=1.2.1",
        
        # Kokoro dependencies
        "phonemizer>=3.2.0",
        "scipy>=1.11.0",
        "munch>=4.0.0",
        "transformers>=4.38.0",
        "torch>=2.0.0",
    ],
    extras_require={
        'cuda': [
            'torch @ https://download.pytorch.org/whl/cu118/torch-2.5.1%2Bcu118-cp310-cp310-linux_x86_64.whl',
        ],
        'cpu': [
            'torch==2.5.1',
        ]
    },
    python_requires=">=3.10",
    description="A storytelling application that converts speech to text, generates stories, and reads them back",
    author="Adrien",
    author_email="adrien.matea.adan@gmail.com",
    url="https://github.com/Additrien/tell_me_a_story_v2",
    
    # Include model files in package data
    package_data={
        "app": [
            "models/kokoro/**/*",
            "models/kokoro/modules/*.py",
        ],
    },
    include_package_data=True,
) 