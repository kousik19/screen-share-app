from tkinter import Tk

import win32gui
from win32gui import SetParent, FindWindow, SetWindowPos
import time
import subprocess


def attach_window(window_class, parent, x, y, width, height):
    child = FindWindow(window_class, None)
    childHwnd = win32gui.FindWindow(None, 'Calculator')
    print(childHwnd)
    print(parent)
    SetParent(parent, childHwnd)
    SetWindowPos(child, 0, x, y, width, height, 0)


def main():
    root = Tk()

    # subprocess.Popen('C:\\Windows\\system32\\notepad.exe')
    # subprocess.Popen('C:\\Windows\\system32\\calc.exe')

    # Give child processes enough time to launch
    time.sleep(2)

    # Get the HWND of the parent window
    parent = int(root.frame(), 16)

    # attach_window('Edit', parent, 0, 0, 400, 200)
    attach_window('Calculator', parent, 0, 205, 420, 320)

    root.geometry('500x500')
    root.mainloop()


if __name__ == '__main__':
    main()