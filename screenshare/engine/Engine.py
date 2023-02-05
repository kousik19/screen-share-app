from pywinauto import Application


def init(title):
    global app
    global app32
    global appUIA
    global screenControls
    app32 = Application(backend="win32").connect(title=title)
    app = app32[title]

    appUIA = Application(backend="uia").connect(title=title)
    descendants = appUIA[title].descendants(control_type="Button")
    screenControls = []
    for elem in descendants:
        elemPos = {elem: elem.rectangle()}
        screenControls.append(elemPos)
