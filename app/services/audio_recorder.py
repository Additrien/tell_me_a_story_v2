import pyaudio
import wave
import os
from typing import Optional, Dict, List
from fastapi import HTTPException
from app.core.config import settings
import threading

class AudioRecorder:
    def __init__(self):
        self.is_recording = False
        self.current_language = None
        # Redirect ALSA errors to /dev/null
        os.environ['ALSA_PYTHON_ERR_HANDLER_TYPE'] = 'null'
        self.audio = pyaudio.PyAudio()
        self.frames = []
        self.stream = None
        self.recording_thread = None
        self._select_input_device()

    def _select_input_device(self) -> None:
        """Find the first working input device."""
        self.device_index = None
        
        print("\nAvailable audio devices:")
        for i in range(self.audio.get_device_count()):
            try:
                info = self.audio.get_device_info_by_index(i)
                print(f"Device {i}: {info['name']} (Inputs: {info['maxInputChannels']})")
            except IOError:
                print(f"Device {i}: <error reading device info>")
        
        # First try the configured device if any
        if settings.AUDIO_DEVICE_INDEX is not None:
            try:
                device_info = self.audio.get_device_info_by_index(settings.AUDIO_DEVICE_INDEX)
                if device_info['maxInputChannels'] > 0:
                    self.device_index = settings.AUDIO_DEVICE_INDEX
                    print(f"\nUsing configured audio device {self.device_index}: {device_info['name']}")
                    return
            except IOError:
                print(f"Warning: Configured device {settings.AUDIO_DEVICE_INDEX} is not available")

        # Otherwise find the first working input device
        for i in range(self.audio.get_device_count()):
            try:
                device_info = self.audio.get_device_info_by_index(i)
                if device_info['maxInputChannels'] > 0:
                    self.device_index = i
                    print(f"\nSelected default audio input device {i}: {device_info['name']}")
                    return
            except IOError:
                continue

        if self.device_index is None:
            raise HTTPException(status_code=500, detail="No working input device found")

    def start_recording(self, language: str) -> None:
        if self.is_recording:
            raise HTTPException(status_code=400, detail="Recording already in progress")
        
        self.frames = []
        self.is_recording = True
        self.current_language = language
        
        try:
            self.stream = self.audio.open(
                format=pyaudio.paInt16,
                channels=1,
                rate=44100,
                input=True,
                input_device_index=self.device_index,
                frames_per_buffer=1024
            )
        except IOError as e:
            self.is_recording = False
            raise HTTPException(status_code=500, detail=f"Failed to start recording: {str(e)}")
        
        self.recording_thread = threading.Thread(target=self._record)
        self.recording_thread.start()

    def stop_recording(self) -> tuple[str, str]:
        if not self.is_recording:
            raise HTTPException(status_code=400, detail="No recording in progress")
        
        self.is_recording = False
        self.recording_thread.join()
        
        if self.stream:
            try:
                self.stream.stop_stream()
                self.stream.close()
            except IOError:
                pass  # Ignore errors during cleanup
        
        # Check if we actually recorded any audio
        if not self.frames:
            raise HTTPException(status_code=400, detail="No audio data was recorded")
            
        # Check minimum recording length (at least 0.5 seconds)
        total_frames = sum(len(frame) for frame in self.frames)
        recording_duration = (total_frames / 2) / 44100  # Convert frames to seconds
        if recording_duration < 0.5:
            raise HTTPException(status_code=400, detail="Recording too short (minimum 0.5 seconds)")
        
        audio_file = "temp_audio.wav"
        with wave.open(audio_file, 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(self.audio.get_sample_size(pyaudio.paInt16))
            wf.setframerate(44100)
            wf.writeframes(b''.join(self.frames))
        
        language = self.current_language
        self.current_language = None  # Reset language
        return audio_file, language

    def _record(self):
        error_count = 0
        max_errors = 5  # Maximum number of consecutive errors before stopping
        total_frames = 0
        
        print(f"Starting recording with device index: {self.device_index}")
        print(f"Device info: {self.audio.get_device_info_by_index(self.device_index)}")
        
        while self.is_recording:
            try:
                data = self.stream.read(1024, exception_on_overflow=False)
                if data:  # Only append if we got actual data
                    self.frames.append(data)
                    total_frames += len(data)
                    if total_frames % (44100 * 2) == 0:  # Log every second
                        print(f"Recording in progress... Total data: {total_frames} bytes")
                    error_count = 0  # Reset error count on successful read
                else:
                    error_count += 1
                    print(f"Warning: Empty data received from microphone")
            except IOError as e:
                print(f"Warning: Recording error occurred: {str(e)}")
                error_count += 1
            
            # Stop recording if we hit too many errors
            if error_count >= max_errors:
                print("Too many recording errors, stopping recording")
                self.is_recording = False
                break
        
        print(f"Recording stopped. Total frames: {len(self.frames)}, Total bytes: {sum(len(frame) for frame in self.frames)}")

    def __del__(self):
        if self.stream:
            try:
                self.stream.close()
            except:
                pass
        try:
            self.audio.terminate()
        except:
            pass

    def list_input_devices(self) -> List[Dict]:
        """List all available input devices."""
        devices = []
        for i in range(self.audio.get_device_count()):
            try:
                device_info = self.audio.get_device_info_by_index(i)
                if device_info['maxInputChannels'] > 0:
                    devices.append({
                        'index': i,
                        'name': device_info['name'],
                        'channels': device_info['maxInputChannels'],
                        'sample_rate': device_info['defaultSampleRate']
                    })
            except IOError:
                continue
        return devices

audio_recorder = AudioRecorder()

async def cleanup_audio_file(file_path: str):
    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"Temporary audio file {file_path} removed.")
