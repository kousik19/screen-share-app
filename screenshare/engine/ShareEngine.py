import ctypes

import win32gui
import win32ui
from ctypes import windll
from PIL import Image
import base64
from io import BytesIO

from desktopmagic.screengrab_win32 import (getDisplayRects, getRectAsImage)

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


def getScreen(title):
    flag = 2
    if flag == 1:
        # hwnd = win32gui.FindWindow(None, 'Kousik, Mandal | 12345 | IOMAX Carotid - Cascade Surgical Studio')
        hwnd = win32gui.FindWindow(None, title)

        # windll.user32.SetProcessDPIAware()
        left, top, right, bot = win32gui.GetClientRect(hwnd)
        w = right - left
        h = bot - top

        hwndDC = win32gui.GetWindowDC(hwnd)
        mfcDC = win32ui.CreateDCFromHandle(hwndDC)
        saveDC = mfcDC.CreateCompatibleDC()

        saveBitMap = win32ui.CreateBitmap()
        saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)

        saveDC.SelectObject(saveBitMap)

        windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(), 2)

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

        buffered = BytesIO()
        im.save(buffered, format="JPEG")
        return base64.b64encode(buffered.getvalue()).decode('UTF-8')
    if flag == 2:
        size = round(ctypes.windll.shcore.GetScaleFactorForDevice(0) / 100 * 32)
        cursor = get_cursor()

        pixdata = cursor.load()
        minsize = [size, None]

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

        screens = (getDisplayRects())
        rect = getRectAsImage(screens[1])

        ratio = ctypes.windll.shcore.GetScaleFactorForDevice(0) / 100
        pos_win = win32gui.GetCursorPos()
        pos = (round(pos_win[0] * ratio), round(pos_win[1] * ratio))
        rect.paste(cursor, pos, cursor)

        output = BytesIO()
        rect.save(output, format='PNG')
        im_data = output.getvalue()
        image_data = base64.b64encode(im_data).decode()
        return image_data
