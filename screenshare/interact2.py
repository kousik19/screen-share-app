import ctypes

import pywinauto
import winxpgui
from PIL.ImageEnhance import Color
from pywinauto import Application
from pywinauto import mouse
import win32api
import win32gui
import win32con
from threading import Thread
from time import sleep
from ctypes.wintypes import tagPOINT

app = Application(backend="win32").connect(path=r"C:\Program Files\Cadwell\Cascade Surgical Studio\Cascade.exe")
appPy = Application(backend='win32').connect(path=r"C:\Program Files\JetBrains\PyCharm 2020.2.5\bin\pycharm64.exe")
appWindow = app[
    'Kousik, Mandal | 12345 | IOMAX Carotid - Cascade Surgical StudioHwndWrapper[Cascade.exe;Main Thread;319b0fe7-6f1d-43d0-8bcf-d1eec6d8e4df]']

# handles = pywinauto.findwindows.find_windows()
# for w_handle in handles:
#     wind = app.window(handle=w_handle)
#     print(wind.texts())

# app.MainDialog.click_input(coords=(953, 656))
# app['Cascade Surgical StudioHwndWrapper[Cascade.exe;Main Thread;d9451551-2d6f-4d10-973d-ab6ad4f37cf2]'].send_keystrokes(str('G'))
# app['Cascade Surgical StudioHwndWrapper[Cascade.exe;Main Thread;d9451551-2d6f-4d10-973d-ab6ad4f37cf2]'].send_keystrokes(str('O'))
# app['Cascade Surgical StudioHwndWrapper[Cascade.exe;Main Thread;d9451551-2d6f-4d10-973d-ab6ad4f37cf2]'].send_keystrokes(str('D'))
# app['Cascade Surgical StudioHwndWrapper[Cascade.exe;Main Thread;d9451551-2d6f-4d10-973d-ab6ad4f37cf2]'].send_keystrokes('{TAB}')
# app['Cascade Surgical StudioHwndWrapper[Cascade.exe;Main Thread;d9451551-2d6f-4d10-973d-ab6ad4f37cf2]'].click_input(coords=(759,251))
# app['Cascade Surgical StudioHwndWrapper[Cascade.exe;Main Thread;d9451551-2d6f-4d10-973d-ab6ad4f37cf2]'].send_keystrokes(str('I'))
# app['Cascade Surgical StudioHwndWrapper[Cascade.exe;Main Thread;d9451551-2d6f-4d10-973d-ab6ad4f37cf2]'].send_keystrokes(str('S'))
# app['Cascade Surgical StudioHwndWrapper[Cascade.exe;Main Thread;d9451551-2d6f-4d10-973d-ab6ad4f37cf2]'].send_keystrokes('{VK_RBUTTON}')
# appPy.top_window().set_focus()
# appWindow.send_keystrokes('{VK_RBUTTON}')

# app32 = Application(backend="win32").connect(path=r"C:\Program Files\Cadwell\Cascade Surgical Studio\Cascade.exe")
# appUIA = Application(backend="uia").connect(path=r"C:\Program Files\Cadwell\Cascade Surgical Studio\Cascade.exe")
# descendants = appUIA['Kousik, Mandal | 12345 | IOMAX Carotid - Cascade Surgical Studio'].descendants(control_type="Image")
#
# print(descendants)
# selectedElem = None
# for elem in descendants:
#     # if elem.rectangle().left != 0 and elem.rectangle().left < 70 and elem.rectangle().top < 200:
#     #     print(elem.rectangle())
#     if elem.rectangle().left == 57 and elem.rectangle().top == 188:
#         selectedElem = elem
#
# app.window().move_window(x=2000, y=1500, width=50, height=50, repaint=True)
# selectedElem.toggle()

hwnd = win32gui.FindWindow(None, "Kousik, Mandal | 12345 | IOMAX Carotid - Cascade Surgical Studio")
appWindow.click_input(coords=(65, 200))
win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, win32con.WS_EX_LAYERED)
ctypes.windll.user32.SetWindowLongPtrW(hwnd, win32con.GWL_EXSTYLE, win32con.WS_EX_LAYERED)
ctypes.windll.user32.SetLayeredWindowAttributes(hwnd, 0, 10, 0x2)
