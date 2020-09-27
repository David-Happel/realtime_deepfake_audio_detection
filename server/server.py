from aiohttp import web
import socketio
import random

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


@sio.event
async def connect(sid, environ):
    print('connect ', sid)
    async with sio.session(sid) as session:
        session['n'] = 0
        session['total'] = 0

@sio.event
async def disconnect(sid):
    print('disconnect ', sid)

## We bind our aiohttp endpoint to our app
## router
app.router.add_get('/', index)

## We kick off our server
if __name__ == '__main__':
    web.run_app(app)