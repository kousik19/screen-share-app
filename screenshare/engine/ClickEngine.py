import win32com
import win32gui
import win32com.client
import pyautogui

from engine import Engine

def clickOnScreen(coords):
    flag = 3
    coords = coords.split('&')
    x = int(coords[0])
    y = int(coords[1])
    if flag == 1:
        print("Preparing for clicking old way")
        Engine.app.click_input(coords=(x, y))
        shell = win32com.client.Dispatch("WScript.Shell")
        shell.SendKeys('%')
        win32gui.SetForegroundWindow(win32gui.FindWindow(None, 'Share Screen - Google Chrome'))
    if flag == 2:
        print("Preparing for clicking new way")
        print(len(Engine.screenControls))
        for control in Engine.screenControls:
            controlElem = list(control.keys())[0]
            position = control.get(controlElem)
            if position.left < x < position.right and position.top < y < position.bottom:
                print("Found a control")
                Engine.app32.window().move_window(x=2000, y=1500, width=1920, height=1016, repaint=True)
                try:
                    controlElem.toggle()
                except:
                    print("Toggle unavailable")
                try:
                    controlElem.click()
                except:
                    print("Click unavailable")
                shell = win32com.client.Dispatch("WScript.Shell")
                shell.SendKeys('%')
                win32gui.SetForegroundWindow(win32gui.FindWindow(None, 'Share Screen - Google Chrome'))
                Engine.app32.window().move_window(x=0, y=0, width=1920, height=1016, repaint=True)
                shell = win32com.client.Dispatch("WScript.Shell")
                shell.SendKeys('%')
                win32gui.SetForegroundWindow(win32gui.FindWindow(None, 'Share Screen - Google Chrome'))
    if flag == 3:
        # currentPosition = pyautogui.position()
        # pyautogui.click(x, y)
        pyautogui.moveTo(x, y)


def rightClickOnScreen(coords):
    print("Remove this method")

def moveMouseBackToBrowser(coords):
    global curX
    global curY
    coords = coords.split('&')
    curX = int(coords[0])
    curY = int(coords[1])
