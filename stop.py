from subprocess import check_output
import pathlib
from desktopmagic.screengrab_win32 import (getDisplayRects)

screens = (getDisplayRects())
if len(screens) == 1:
    print("Already Stopped")
    exit()

path = pathlib.Path(__file__).parent.resolve().__str__()
check_output(path + "/mmt/MultiMonitorTool.exe /SetPrimary 1", shell=True)
check_output(path + "/VirtualScreenDriver/deviceinstaller64.exe enableidd 0", shell=True)
