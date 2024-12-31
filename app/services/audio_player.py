import pyaudio
import numpy as np
from app.core.config import settings

async def play_audio(audio_data: bytes):
    p = pyaudio.PyAudio()
    
    # Convert bytes to numpy array
    audio_array = np.frombuffer(audio_data, dtype=np.int16)
    
    # Open stream
    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=settings.MMS_SAMPLE_RATE,
                    output=True)
    
    # Play audio
    stream.write(audio_array.tobytes())
    
    # Close stream
    stream.stop_stream()
    stream.close()
    p.terminate()