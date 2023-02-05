from engine import Engine


def typeOnScreen(char):
    print("Preparing for typing")
    Engine.app.send_keystrokes(str(char))
