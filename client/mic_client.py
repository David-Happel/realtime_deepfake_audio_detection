import socketio
import pyaudio
import sys
import socket
import time
# import numpy
sio = socketio.Client()

guesses = []
emit_times = dict()


@ sio.on('response')
def message(data):
    guesses.append([data['n'], data['guess'], data['avg']])
    time_passed = time.perf_counter() - emit_times[data['n']]
    print('guess: ', data['n'], data['guess'], 'avg:', data['avg'], "time:", time_passed)


@ sio.event
def connect():
    print("I'm connected!")


@ sio.event
def connect_error():
    print("The connection failed!")


@ sio.event
def disconnect():
    stream.stop_stream()
    stream.close()
    audio.terminate()
    print(" ")
    for row in guesses:
        print(', '.join(map(str, row)))

    print("disconnected!")


# Server connection
port = '8080'
print("Server Connecting to server on port " + port)
sio.connect('http://localhost:' + port)
print('my sid is', sio.sid)

# AUDIO Input
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
RECORD_SECONDS = 3

audio = pyaudio.PyAudio()

# start Recording
stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK)
print("recording...")
frames = []

n = 0
while True:
    n += 1
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        sio.emit('audio', {'data': data, 'id': i})
        # print(i)
    print("finished recording:", n)
    emit_times[n] = time.perf_counter()
