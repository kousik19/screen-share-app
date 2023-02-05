import win32api
import win32gui
import win32con

hwnd = win32gui.FindWindow(None, "Cascade Surgical Studio1")

win32gui.SetWindowLong (hwnd, win32con.GWL_EXSTYLE, win32con.WS_EX_LAYERED)
win32gui.SetLayeredWindowAttributes(hwnd, win32api.RGB(0,0,0), 180, win32con.LWA_ALPHA)