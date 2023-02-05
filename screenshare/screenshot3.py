from __future__ import print_function
import desktopmagic
from desktopmagic.screengrab_win32 \
import (getDisplayRects, saveScreenToBmp, getScreenAsImage, getRectAsImage, getDisplaysAsImages)

screens = (getDisplayRects())
rect = getRectAsImage(screens[1])
rect.save('leftscr.png', format='png')