import socketio


sio = socketio.Client()
#Server connection
port = 5000
print("Server Connecting to server on port " + port)
sio.connect('http://localhost:' + port)
print('my sid is', sio.sid)


#Events
@sio.event
def message(data):
    print('I received a message!')

@sio.event
def connect():
    print("I'm connected!")
    

@sio.event
def connect_error():
    print("The connection failed!")

@sio.event
def disconnect():
    print("I'm disconnected!")


#Emit events
sio.emit('my message', {'foo': 'bar'})

