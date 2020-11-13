

import random
import wave
import pyaudio
import sys
import socket
import asyncio
from sio import sio, run_server
from processing import process_audio
from config import FORMAT, CHANNELS, RATE, CHUNK, RECORD_SECONDS, TOTAL_CHUNKS
from threading import Thread


@sio.on('message')
async def print_message(sid, message):

    print("Socket ID: ", sid)
    print(message)
    await sio.emit('message', message)


@sio.on('audio')
async def process_data(sid, data):
    async with sio.session(sid) as session:
        session['frames'].append(data['data'])
        # print(data['id'], len(session['frames']), " / ", TOTAL_CHUNKS)
        if len(session['frames']) == TOTAL_CHUNKS:
            # Spawn new thread
            t = Thread(target=asyncio.run, args=(process_audio(sid, session['n'], session['frames']), ))
            t.start()

            session['n'] += 1
            session['frames'] = []


@ sio.event
async def connect(sid, environ):
    print('connect ', sid)
    async with sio.session(sid) as session:
        # Set inital session variables
        session['n'] = 1
        session['total'] = 0
        session['frames'] = []


@ sio.event
async def disconnect(sid):
    print('disconnect ', sid)

if __name__ == '__main__':
    run_server()
