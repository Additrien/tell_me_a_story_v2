from setuptools import setup, find_packages

setup(
    name="tell_me_a_story",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        # Core dependencies
        "fastapi==0.115.2",
        "uvicorn==0.32.0",
        "python-multipart==0.0.12",
        "pydantic-settings==2.6.0",
        "pyyaml==6.0.2",
        
        # Audio processing
        "pyaudio==0.2.14",
        "soundfile==0.12.1",
        "librosa==0.9.1",
        "SpeechRecognition==3.11.0",
        
        # HTTP client
        "aiohttp==3.11.11",
        
        # Base ML dependencies
        "numpy>=1.24.3",
        "transformers>=4.38.0",
        "datasets>=2.18.0",
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
) 