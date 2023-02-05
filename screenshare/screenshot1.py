import time
import pywinauto

app = pywinauto .Application(backend="win32").start(r"C:\WINDOWS\system32\notepad.exe")

time.sleep(2)
print('sleeping over')
Wizard = app['Untitled - Notepad']

while True:
    Wizard.send_keystrokes("{VK_NEXT}")
    time.sleep(1)
