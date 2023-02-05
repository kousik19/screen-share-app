import socketio
import sys

sys.path.append("..")
from utils.GetApps import getWindows
from engine.ShareEngine import getScreen
from engine.TypeEngine import typeOnScreen
from engine.ClickEngine import clickOnScreen, rightClickOnScreen
from engine import Engine

server_url = 'http://localhost:3000'
sio = socketio.Client()

@sio.on('GetAppList')
def message(data):
    windows = getWindows()
    sio.emit('AppListResponse', windows)

@sio.on('ChangeApp')
def message(data):
    Engine.init(data)

@sio.on('ShareScreen')
def message(data):
    screen = getScreen(data)
    sio.emit('CurrentScreen', screen)


@sio.on('TypeRequest')
def message(data):
    typeOnScreen(data)

@sio.on('ClickRequest')
def message(data):
    clickOnScreen(data)

@sio.on('RightClickRequest')
def message(data):
    rightClickOnScreen(data)

@sio.event
def connect():
    print("Connected!")


sio.connect(server_url)
