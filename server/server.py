from aiohttp import web
import socketio
import random
import wave
import pyaudio, sys, socket

## creates a new Async Socket IO Server
sio = socketio.AsyncServer()
## Creates a new Aiohttp Web Application
app = web.Application()
# Binds our Socket.IO server to our Web App
## instance
sio.attach(app)

## we can define aiohttp endpoints just as we normally
## would with no change
async def index(request):
    with open('index.html') as f:
        return web.Response(text=f.read(), content_type='text/html')

## If we wanted to create a new websocket endpoint,
## use this decorator, passing in the name of the
## event we wish to listen out for
@sio.on('message')
async def print_message(sid, message):
    ## When we receive a new event of type
    ## 'message' through a socket.io connection
    ## we print the socket ID and the message
    print("Socket ID: " , sid)
    print(message)
    await sio.emit('message', message)

@sio.on('data')
async def process_data(sid, data):
    async with sio.session(sid) as session:
        print("Socket ID data: " , sid, 'n:', session['n'])
        print(data)
        session['n'] += 1
        session['total'] += random.randint(0,100)
        await sio.emit('response', session['total']/session['n'])

@sio.on('audio')
async def process_data(sid, data):
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    CHUNK = 1024
    RECORD_SECONDS = 5
    TOTAL_CHUNKS = int(RATE / CHUNK * RECORD_SECONDS)

    async with sio.session(sid) as session:
        session['frames'].append(data['data'])
        print(len(session['frames']), " / ", TOTAL_CHUNKS)
        if len(session['frames']) == TOTAL_CHUNKS:
            print("done")
            audio = pyaudio.PyAudio()

            WAVE_OUTPUT_FILENAME = "audio/"+str(session['n'])+"_file.wav"
            waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')

            waveFile.setnchannels(CHANNELS)
            waveFile.setsampwidth(audio.get_sample_size(FORMAT))
            waveFile.setframerate(RATE)
            waveFile.writeframes(b''.join(session['frames']))

            print(waveFile.getnchannels(), waveFile.getsampwidth(), waveFile.getframerate(), waveFile.getnframes())
            waveFile.close()

            session['n'] += 1
            session['frames'] = []

        
@sio.event
async def connect(sid, environ):
    print('connect ', sid)
    async with sio.session(sid) as session:
        session['n'] = 0
        session['total'] = 0
        session['frames'] = []

@sio.event
async def disconnect(sid):
    print('disconnect ', sid)

## We bind our aiohttp endpoint to our app
## router
app.router.add_get('/', index)

## We kick off our server
if __name__ == '__main__':
    web.run_app(app)