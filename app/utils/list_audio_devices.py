import pyaudio

def list_audio_devices():
    p = pyaudio.PyAudio()
    info = p.get_host_api_info_by_index(0)
    num_devices = info.get('deviceCount')

    for i in range(num_devices):
        device = p.get_device_info_by_index(i)
        print(f"Device {i}: {device.get('name')}")

    p.terminate()

if __name__ == "__main__":
    list_audio_devices()

