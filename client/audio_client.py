import socketio
import pyaudio
import sys
import socket
sio = socketio.Client()
# Events


@sio.on('response')
def message(data):
    print('guess: ', data['guess'])


@sio.event
def connect():
    print("I'm connected!")


@sio.event
def connect_error():
    print("The connection failed!")


@sio.event
def disconnect():
    print("I'm disconnected!")


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
RECORD_SECONDS = 5

audio = pyaudio.PyAudio()

# start Recording
stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK)
print("recording...")
frames = []

while True:
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        sio.emit('audio', {'data': data, 'id': i})
        print(i)
    print("finished recording")
