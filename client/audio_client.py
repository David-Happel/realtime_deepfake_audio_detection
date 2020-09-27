import socketio
import pyaudio, sys, socket
sio = socketio.Client()
#Events
@sio.on('message')
def message(data):
    print('I received a message!', data)

#Events
@sio.on('response')
def message(data):
    print('Response: ', data)

@sio.event
def connect():
    print("I'm connected!")
    

@sio.event
def connect_error():
    print("The connection failed!")

@sio.event
def disconnect():
    print("I'm disconnected!")

#Server connection
port = '8080'
print("Server Connecting to server on port " + port)
sio.connect('http://localhost:' + port)
print('my sid is', sio.sid)


#Emit events
# sio.emit('data', {'data': '010010'})

#AUDIO Input
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "file.wav"

audio = pyaudio.PyAudio()

# start Recording
stream = audio.open(format=FORMAT, channels=CHANNELS,
                rate=RATE, input=True,
                frames_per_buffer=CHUNK)
print("recording...")
frames = []

for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    sio.emit('audio', {'data': data})
    print(data)
print("finished recording")
