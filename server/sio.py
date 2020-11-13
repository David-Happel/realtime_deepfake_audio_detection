from aiohttp import web
import socketio


async def index(request):
    with open('index.html') as f:
        return web.Response(text=f.read(), content_type='text/html')

# creates a new Async Socket IO Server
sio = socketio.AsyncServer()

# Creates a new Aiohttp Web Application
app = web.Application()

# Binds our Socket.IO server to our Web App
# instance
sio.attach(app)

# We bind our aiohttp endpoint to our app
# router
app.router.add_get('/', index)


def run_server():
    web.run_app(app)
