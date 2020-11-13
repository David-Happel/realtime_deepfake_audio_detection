
import pyaudio
import wave
import time
import random
from spectogrammer import file_to_spectogram, spectogram_to_db, save_spectogram
from config import FORMAT, CHANNELS, RATE, CHUNK, RECORD_SECONDS, TOTAL_CHUNKS
from sio import sio

# This is the main function that is called as a new thread each time a new full audio clip has been received.
# It does all the processing and calls the model.


async def process_audio(sid, n, frames):
    print("processing")

    filename = "audio/"+str(n)+"_file.wav"
    save_audio_to_wav(frames, filename)

    # Process audio file
    guess = fake_model(filename)

    async with sio.session(sid) as session:
        session['total'] += guess
        avg = session['total'] / n

    # Set response of to the specific session.
    await sio.emit('response', {'guess': guess, 'avg': avg, 'n': n}, room=sid)
    print("prediction:", guess)

    # spectogram, sr = file_to_spectogram(filename)
    # spectogram = spectogram_to_db(spectogram)
    # save_spectogram(spectogram, sr, filename)


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


def fake_model(filename):
    time.sleep(5)
    return (random.random() * 0.5) + 0.3
