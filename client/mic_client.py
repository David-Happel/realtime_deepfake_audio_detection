import socketio
import pyaudio
import sys
import socket
import time
from config import FORMAT, RATE, CHUNK, TOTAL_CHUNKS, CHANNELS
# import numpy


def audo_client():
    sio = socketio.Client()
    running = True

    guesses = []
    emit_times = dict()

    @ sio.on('response')
    def message(data):
        time_passed = time.perf_counter() - emit_times[data['n']]
        guesses.append([data['n'], data['guess'], data['avg'], time_passed])
        print('guess:', data['n'], data['guess'], 'avg:', data['avg'], "time:", time_passed)
        if int(data['n']) == 10:
            nonlocal running
            running = False

    @ sio.event
    def connect():
        print("I'm connected!")

    @ sio.event
    def connect_error():
        print("The connection failed!")

    @ sio.event
    def disconnect():
        clean_up(stream, audio, guesses)
        print("disconnected!")

    # Server connection
    port = '8080'
    print("Server Connecting to server on port " + port)
    sio.connect('http://localhost:' + port)
    print('my sid is', sio.sid)

    audio = pyaudio.PyAudio()

    # start Recording
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)
    print("recording...")
    frames = []

    n = 0
    while running:
        if n < 11:
            n += 1
            for i in range(0, TOTAL_CHUNKS):
                data = stream.read(CHUNK)
                sio.emit('audio', {'data': data, 'id': i})
                # print(i)
            print("finished recording:", n)
            emit_times[n] = time.perf_counter()

    sio.disconnect()
    clean_up(stream, audio, guesses)


def clean_up(stream, audio, guesses):
    stream.stop_stream()
    stream.close()
    audio.terminate()
    print(" ")
    for row in guesses:
        print(', '.join(map(str, row)))


if __name__ == "__main__":
    audo_client()
