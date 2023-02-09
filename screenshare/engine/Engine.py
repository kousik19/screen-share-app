import ctypes

import win32process
from pynput.keyboard import Key, Controller

import win32gui
import win32ui
from PIL import Image
import keyboard

from subprocess import check_output
import pathlib
from desktopmagic.screengrab_win32 import (getDisplayRects)
from threading import Thread
import time


def init():
    global screens
    global size
    global cursor
    global ratio
    global activeApp
    screens = (getDisplayRects())
    size = round(ctypes.windll.shcore.GetScaleFactorForDevice(0) / 100 * 32)
    cursor = get_cursor()
    ratio = ctypes.windll.shcore.GetScaleFactorForDevice(0) / 100
    thread = Thread(target=checkKey)
    thread2 = Thread(target=checkApp)
    thread.start()
    thread2.start()


def checkKey():
    while True:
        if keyboard.read_key() == "esc":
            time.sleep(.5)
            # ctypes.windll.user32.SetCursorPos(-1200, 300)
            ctypes.windll.user32.SetCursorPos(500, 500)


def checkApp():
    keyboard = Controller()
    activeApp = ''
    appsInVirtualScreen = []
    while True:
        try:
            time.sleep(.5)
            w = win32gui
            name = w.GetWindowText(w.GetForegroundWindow())
            hwnd = win32gui.FindWindow(None, name)
            threadid, pid = win32process.GetWindowThreadProcessId(hwnd)
            if activeApp == pid or "chrome" in name.lower() or appsInVirtualScreen.count(pid) > 1:
                continue
            pos_win = win32gui.GetCursorPos()
            if pos_win[0] > 1942:
                activeApp = pid
                appsInVirtualScreen.append(pid)
                keyboard.press(Key.cmd)
                keyboard.press(Key.shift)
                keyboard.press(Key.right)
                keyboard.release(Key.cmd)
                keyboard.release(Key.shift)
                keyboard.release(Key.right)
        except():
            print("Error")


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


def start():
    screens = (getDisplayRects())
    if len(screens) > 1:
        print("Already Started")
        exit()

    print("Creating virtual screen...")
    path = pathlib.Path(__file__).parent.resolve().__str__()
    check_output(path + "/../../VirtualScreenDriver/deviceinstaller64.exe enableidd 1", shell=True)
    check_output(path + "/../../mmt/MultiMonitorTool.exe /SetNextPrimary", shell=True)
    print("Virtual screen created...")


def stop():
    screens = (getDisplayRects())
    if len(screens) == 1:
        print("Already Stopped")
        exit()

    path = pathlib.Path(__file__).parent.resolve().__str__()
    check_output(path + "/../../mmt/MultiMonitorTool.exe /SetPrimary 1", shell=True)
    check_output(path + "/../../VirtualScreenDriver/deviceinstaller64.exe enableidd 0", shell=True)
