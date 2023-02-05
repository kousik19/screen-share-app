import win32gui

apps = []
ignoredApps = ['ABC']


def getApps(hwnd, *args) -> list:
    global apps
    if win32gui.IsWindowVisible(hwnd):
        title = win32gui.GetWindowText(hwnd)
        if not title == '':
            if not title in apps and not title in ignoredApps:
                apps.append(title)


def getWindows():
    win32gui.EnumWindows(getApps, '')
    return apps
