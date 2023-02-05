import win32api
import win32gui
import win32ui
import win32con
from ctypes import windll
from PIL import Image
from pywinauto import application


def type(handle, param):
    print(win32gui.GetClassName(handle) == param)
    if win32gui.GetClassName(handle) == param:
        win32gui.SendMessage(handle, win32con.WM_CHAR, ord('G'), 0)
        win32gui.SendMessage(handle, win32con.WM_CHAR, ord('O'), 0)
        win32gui.SendMessage(handle, win32con.WM_CHAR, ord('D'), 0)
        win32gui.SendMessage(handle, win32con.WM_CHAR, ord(' '), 0)
        win32gui.SendMessage(handle, win32con.WM_CHAR, ord('I'), 0)
        win32gui.SendMessage(handle, win32con.WM_CHAR, ord('S'), 0)
        win32gui.SendMessage(handle, win32con.WM_CHAR, ord(' '), 0)
        win32gui.SendMessage(handle, win32con.WM_CHAR, ord('G'), 0)
        win32gui.SendMessage(handle, win32con.WM_CHAR, ord('R'), 0)
        win32gui.SendMessage(handle, win32con.WM_CHAR, ord('E'), 0)
        win32gui.SendMessage(handle, win32con.WM_CHAR, ord('A'), 0)
        win32gui.SendMessage(handle, win32con.WM_CHAR, ord('T'), 0)


def typeNew(handle, param):
    print(handle)
    win32gui.SendMessage(handle, win32con.MB_DEFBUTTON1, ord('G'), 0)


hwnd = win32gui.FindWindow(None, 'Cascade Surgical Studio')
# win32gui.EnumChildWindows(hwnd, type, 'Edit')

windll.user32.SetProcessDPIAware()
left, top, right, bot = win32gui.GetClientRect(hwnd)
#left, top, right, bot = win32gui.GetWindowRect(hwnd)
w = right - left
h = bot - top
print(w)
print(h)

hwndDC = win32gui.GetWindowDC(hwnd)
mfcDC = win32ui.CreateDCFromHandle(hwndDC)
saveDC = mfcDC.CreateCompatibleDC()

saveBitMap = win32ui.CreateBitmap()
saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)

saveDC.SelectObject(saveBitMap)

# Change the line below depending on whether you want the whole window
# or just the client area.
# result = windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(), 1)
result = windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(), 2)
print(result)

bmpinfo = saveBitMap.GetInfo()
bmpstr = saveBitMap.GetBitmapBits(True)

im = Image.frombuffer(
    'RGB',
    (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
    bmpstr, 'raw', 'BGRX', 0, 1)

win32gui.DeleteObject(saveBitMap.GetHandle())
saveDC.DeleteDC()
mfcDC.DeleteDC()
win32gui.ReleaseDC(hwnd, hwndDC)

if result == 1:
    # PrintWindow Succeeded
    im.save("test.png")
