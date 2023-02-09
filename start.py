from subprocess import check_output
import pathlib
from desktopmagic.screengrab_win32 import (getDisplayRects)
from threading import Thread
import webbrowser
import time
import pygetwindow as gw

def startNodeApp():
    check_output("cd \"screenshare-server\" & npm install", shell=True)
    check_output("node " + path + "/screenshare-server/server.js", shell=True)


def startPythonApp():
    check_output("cd \"screenshare\communication\" & python " + path + "/screenshare/communication/ClientInterface.py", shell=True)

screens = (getDisplayRects())
if len(screens) > 1:
    print("Already Started")
    exit()

print("Creating virtual screen...")
path = pathlib.Path(__file__).parent.resolve().__str__()
check_output(path + "/VirtualScreenDriver/deviceinstaller64.exe enableidd 1", shell=True)
# check_output(path + "/mmt/MultiMonitorTool.exe /SetNextPrimary", shell=True)
print("Virtual screen created...")

nodeApp = Thread(target=startNodeApp)
pythonApp = Thread(target=startPythonApp)
print("Starting Node App...")
nodeApp.start()
print("Waiting...")
time.sleep(5)
print("Starting Python App...")
pythonApp.start()
print("Ready to go... Open in browser: http://localhost:3000/ui/index.html")