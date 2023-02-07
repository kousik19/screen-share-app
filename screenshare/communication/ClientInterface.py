import socketio
import sys

sys.path.append("..")
from engine.ShareEngine import getScreen
from engine import Engine

server_url = 'http://localhost:3000'
sio = socketio.Client()
Engine.init()

@sio.on('ShareScreen')
def message(data):
    screen = getScreen(data)
    sio.emit('CurrentScreen', screen)

@sio.event
def connect():
    print("Connected!")


sio.connect(server_url)
