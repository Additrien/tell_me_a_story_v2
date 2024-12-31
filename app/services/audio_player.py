import pyaudio
import numpy as np
from typing import AsyncIterator, Union
from app.core.config import settings

async def play_audio(audio_data: Union[bytes, AsyncIterator[bytes]]):
    p = pyaudio.PyAudio()
    
    # Open stream
    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=settings.TTS_SAMPLE_RATE,
                    output=True)
    
    try:
        if isinstance(audio_data, bytes):
            # Handle single audio chunk
            audio_array = np.frombuffer(audio_data, dtype=np.int16)
            stream.write(audio_array.tobytes())
        else:
            # Handle streaming audio chunks
            async for chunk in audio_data:
                audio_array = np.frombuffer(chunk, dtype=np.int16)
                stream.write(audio_array.tobytes())
    finally:
        # Close stream
        stream.stop_stream()
        stream.close()
        p.terminate()