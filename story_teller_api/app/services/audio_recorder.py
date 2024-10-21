import speech_recognition as sr
import pyaudio
import wave
import os
from typing import Optional
from fastapi import HTTPException

def record_audio(trigger_word: str = "start", timeout: int = 5, phrase_time_limit: int = 10) -> Optional[str]:
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        print(f"Listening for trigger word: '{trigger_word}'...")

        try:
            audio = recognizer.listen(source, timeout=timeout)
            text = recognizer.recognize_google(audio).lower()

            if trigger_word in text:
                print("Trigger word detected. Starting recording...")
                audio = recognizer.listen(source, phrase_time_limit=phrase_time_limit)
                
                audio_file = "temp_audio.wav"
                with open(audio_file, "wb") as f:
                    f.write(audio.get_wav_data())
                
                print(f"Recording saved to {audio_file}")
                return audio_file
            else:
                print("Trigger word not detected. Please try again.")
                return None

        except sr.WaitTimeoutError:
            print("Timeout: No speech detected")
            return None
        except sr.UnknownValueError:
            print("Speech not understood")
            return None
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
            raise HTTPException(status_code=500, detail="Speech recognition service unavailable")

async def cleanup_audio_file(file_path: str):
    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"Temporary audio file {file_path} removed.")