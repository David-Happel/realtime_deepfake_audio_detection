import pyaudio

# File with all the config values.
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
RECORD_SECONDS = 10
TOTAL_CHUNKS = int(RATE / CHUNK * RECORD_SECONDS)
