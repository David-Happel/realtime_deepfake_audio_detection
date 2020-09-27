import socketio

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
sio.emit('data', {'data': '010010'})
