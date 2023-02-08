import socketio
import sys

sys.path.append("..")
from engine.ClickEngine import clickOnScreen
from engine.ShareEngine import getScreen
from engine import Engine

server_url = 'http://localhost:3000'
sio = socketio.Client()
Engine.init()

@sio.on('ShareScreen')
def message(data):
    screen = getScreen(data)
    sio.emit('CurrentScreen', screen)

@sio.on('ClickRequest')
def message(data):
    clickOnScreen(data)

@sio.on('StartRequest')
def message(data):
    Engine.start()

@sio.on('StopRequest')
def message(data):
    Engine.stop()

@sio.event
def connect():
    print("Connected!")


sio.connect(server_url)
