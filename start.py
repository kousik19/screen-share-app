import atexit
import signal

from subprocess import check_output
import pathlib

path = pathlib.Path(__file__).parent.resolve().__str__()
check_output("pip install -r screenshare/requirements.txt", shell=True)

from screenshare.engine.Monitor import get_virtual_display_name
from threading import Thread
import time


def startNodeApp():
    check_output("cd \"screenshare-server\" & npm install", shell=True)
    check_output("node " + path + "/screenshare-server/server.js", shell=True)


def startPythonApp():
    check_output("cd \"screenshare\communication\" & python " + path + "/screenshare/communication/ClientInterface.py",
                 shell=True)


path = pathlib.Path(__file__).parent.resolve().__str__()
print("Installing...")
check_output(
    path + "/VirtualScreenDriver/deviceinstaller64.exe install " + path + "/VirtualScreenDriver/usbmmidd.inf usbmmidd",
    shell=True)

print("Resetting...")
check_output(path + "/mmt/MultiMonitorTool.exe /SetPrimary 1", shell=True)
check_output(path + "/VirtualScreenDriver/deviceinstaller64.exe enableidd 0", shell=True)

print("Creating virtual screen...")
check_output(path + "/VirtualScreenDriver/deviceinstaller64.exe enableidd 1", shell=True)
# check_output(path + "/mmt/MultiMonitorTool.exe /SetNextPrimary", shell=True)
print("Virtual screen created...")

print("Setting resolution...")
virtual_display_name = get_virtual_display_name()
check_output(path + "/mmt/MultiMonitorTool.exe /setmax \\\\." + virtual_display_name, shell=True)

print("Extending displays...")
check_output("%windir%\System32\DisplaySwitch.exe /extend", shell=True)

nodeApp = Thread(target=startNodeApp)
pythonApp = Thread(target=startPythonApp)
print("Starting Node App...")
nodeApp.start()
print("Waiting...")
time.sleep(5)
print("Starting Python App...")
pythonApp.start()
print("Ready to go... Open in browser: http://localhost:3000/ui/index.html")


def goodbye(path):
    print("Bye bye")
    check_output(path + "/mmt/MultiMonitorTool.exe /SetPrimary 1", shell=True)
    check_output(path + "/VirtualScreenDriver/deviceinstaller64.exe enableidd 0", shell=True)


atexit.register(goodbye, path)
signal.signal(signal.SIGTERM, goodbye)
signal.signal(signal.SIGINT, goodbye)
