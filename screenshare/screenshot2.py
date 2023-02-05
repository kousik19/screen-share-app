import win32gui
import win32ui
import win32con
from ctypes import windll
from PIL import Image, ImageGrab

hwnd = win32gui.FindWindow(None, 'new 2 - Notepad++')

# Change the line below depending on whether you want the whole window
# or just the client area.
#left, top, right, bot = win32gui.GetClientRect(hwnd)
left, top, right, bot = win32gui.GetWindowRect(hwnd)

im = ImageGrab.grab(win32gui.GetWindowRect(hwnd))
im.save("test1.png")
