import ctypes

import pythoncom
import win32process
import wmi

import win32gui
import win32ui
from PIL import Image
import keyboard

from subprocess import check_output
import pathlib
from desktopmagic.screengrab_win32 import (getDisplayRects)
from threading import Thread
import time

from engine.Monitor import get_virtual_display_name

from pynput import mouse


class MouseIOException(Exception): pass


def init():
    global screens
    global size
    global cursor
    global ratio
    global virtual_display_name
    path = pathlib.Path(__file__).parent.resolve().__str__()
    virtual_display_name = get_virtual_display_name(path)
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


def get_app_name(pid):
    pythoncom.CoInitialize()
    c = wmi.WMI()
    try:
        for p in c.query('SELECT Name FROM Win32_Process WHERE ProcessId = %s' % str(pid)):
            exe = p.Name
            break
    except:
        return None
    else:
        return exe


def handle_click(x, y, button, pressed):
    handle_click_thread = Thread(target=handle_screen_switch, args=(x, y, button, pressed))
    handle_click_thread.start()


def handle_screen_switch(x, y, button, pressed):
    global active_app
    global apps_in_virtual_screen
    try:
        active_app
    except:
        active_app = ''
        apps_in_virtual_screen = []
    try:
        time.sleep(1)
        app_window_name = win32gui.GetWindowText(win32gui.GetForegroundWindow())
        hwnd = win32gui.FindWindow(None, app_window_name)
        _, pid = win32process.GetWindowThreadProcessId(hwnd)
        process_name = get_app_name(pid)

        path = pathlib.Path(__file__).parent.resolve().__str__()

        if "chrome" in app_window_name.lower() or active_app == pid:
            return

        active_app = pid

        if x < 1942:
            if apps_in_virtual_screen.count(pid) > 0:
                apps_in_virtual_screen.remove(pid)
                move_to_primary_screen(path, process_name)

        elif x > 1942:
            if apps_in_virtual_screen.count(pid) == 0:
                apps_in_virtual_screen.append(pid)
                move_to_virtual_screen(path, process_name)
    except():
        print("Error")


def checkApp():
    listener = mouse.Listener(on_click=handle_click)
    listener.start()
    listener.join()


def move_to_virtual_screen(path, app_title):
    check_output(
        path + "/../../mmt/MultiMonitorTool.exe /MoveWindow \\\\." + virtual_display_name + " Process " + app_title,
        shell=True)


def move_to_primary_screen(path, app_title):
    check_output(path + "/../../mmt/MultiMonitorTool.exe /MoveWindow Primary Process " + app_title, shell=True)


def get_cursor():
    hcursor = win32gui.GetCursorInfo()[1]
    hdc = win32ui.CreateDCFromHandle(win32gui.GetDC(0))
    hbmp = win32ui.CreateBitmap()
    hbmp.CreateCompatibleBitmap(hdc, 36, 36)
    hdc = hdc.CreateCompatibleDC()
    hdc.SelectObject(hbmp)
    hdc.DrawIcon((0, 0), hcursor)

    bmpinfo = hbmp.GetInfo()
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
    print("Creating virtual screen...")
    path = pathlib.Path(__file__).parent.resolve().__str__()
    check_output(path + "/../../mmt/MultiMonitorTool.exe /enable  \\\\." + virtual_display_name, shell=True)
    print("Virtual screen created...")


def stop():
    global virtual_display_name
    path = pathlib.Path(__file__).parent.resolve().__str__()
    check_output(path + "/../../mmt/MultiMonitorTool.exe /disable \\\\." + virtual_display_name, shell=True)
