from time import sleep
import win32gui
import win32con


def callback(handle, param):
    s = win32gui.GetClassName(handle)
    try:
        print(f'Sending key to {handle}, {s}')
        win32gui.SendMessage(handle, win32con.WM_KEYDOWN, win32con.VK_NEXT, 0)
        win32gui.SendMessage(handle, win32con.WM_KEYUP, win32con.VK_NEXT, 0)
    except Exception:
        print('Exception sending to {handle}, {s}')


hwnd = win32gui.FindWindow(None, "Cascade Surgical Studio")
win32gui.EnumWindows(callback, 0)
