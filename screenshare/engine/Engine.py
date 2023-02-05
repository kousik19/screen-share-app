import ctypes

import win32gui
import win32ui
from PIL import Image
from desktopmagic.screengrab_win32 import (getDisplayRects, getRectAsImage)

def init():
    global screens
    global size
    global cursor
    global ratio
    screens = (getDisplayRects())
    size = round(ctypes.windll.shcore.GetScaleFactorForDevice(0) / 100 * 32)
    cursor = get_cursor()
    ratio = ctypes.windll.shcore.GetScaleFactorForDevice(0) / 100

def get_cursor():
    hcursor = win32gui.GetCursorInfo()[1]
    hdc = win32ui.CreateDCFromHandle(win32gui.GetDC(0))
    hbmp = win32ui.CreateBitmap()
    hbmp.CreateCompatibleBitmap(hdc, 36, 36)
    hdc = hdc.CreateCompatibleDC()
    hdc.SelectObject(hbmp)
    hdc.DrawIcon((0, 0), hcursor)

    bmpinfo = hbmp.GetInfo()
    bmpbytes = hbmp.GetBitmapBits()
    bmpstr = hbmp.GetBitmapBits(True)
    cursor = Image.frombuffer('RGB', (bmpinfo['bmWidth'], bmpinfo['bmHeight']), bmpstr, 'raw', 'BGRX', 0, 1).convert(
        "RGBA")

    win32gui.DestroyIcon(hcursor)
    win32gui.DeleteObject(hbmp.GetHandle())
    hdc.DeleteDC()

    pixdata = cursor.load()
    minsize = [32, None]

    width, height = cursor.size
    for y in range(height):
        for x in range(width):

            if pixdata[x, y] == (0, 0, 0, 255):
                pixdata[x, y] = (0, 0, 0, 0)

            else:
                if minsize[1] == None:
                    minsize[1] = y

                if x < minsize[0]:
                    minsize[0] = x

    return cursor
