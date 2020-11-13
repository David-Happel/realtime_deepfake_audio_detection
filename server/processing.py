
import pyaudio
import wave
import time
import random
from spectogrammer import file_to_spectogram, spectogram_to_db, save_spectogram
from config import FORMAT, CHANNELS, RATE, CHUNK, RECORD_SECONDS, TOTAL_CHUNKS
from sio import sio


async def process_audio(sid, n, frames):
    print("processing")

    filename = "audio/"+str(n)+"_file.wav"
    save_audio_to_wav(frames, filename)

    # Process audio file
    guess = fake_model()
    await sio.emit('response', {'guess': guess, 'n': n}, room=sid)
    print("prediction:", guess)

    spectogram, sr = file_to_spectogram(filename)
    spectogram = spectogram_to_db(spectogram)
    save_spectogram(spectogram, sr, filename)


def save_audio_to_wav(frames, filename):
    audio = pyaudio.PyAudio()
    waveFile = wave.open(filename, 'wb')

    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(audio.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(frames))

    # print(waveFile.getnchannels(), waveFile.getsampwidth(), waveFile.getframerate(), waveFile.getnframes())
    waveFile.close()
    return


def fake_model():
    time.sleep(5)
    return (random.random() * 0.5) + 0.3
