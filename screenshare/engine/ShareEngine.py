import ctypes

import win32gui
import win32ui
from ctypes import windll
from PIL import Image
import base64
from io import BytesIO

from engine import Engine

from desktopmagic.screengrab_win32 import (getDisplayRects, getRectAsImage)

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

        cursor = Engine.cursor
        rect = getRectAsImage(Engine.screens[1])
        pos_win = win32gui.GetCursorPos()
        pos = (round(pos_win[0] * Engine.ratio), round(pos_win[1] * Engine.ratio))
        rect.paste(cursor, pos, cursor)

        output = BytesIO()
        rect.save(output, format='JPEG')
        im_data = output.getvalue()
        image_data = base64.b64encode(im_data).decode()
        return image_data
