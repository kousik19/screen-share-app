import pathlib
from subprocess import check_output
import os
from chardet import detect
import linecache


def get_encoding_type(file):
    with open(file, 'rb') as f:
        rawdata = f.read()
    return detect(rawdata)['encoding']


def get_virtual_display_name(path):
    path = pathlib.Path(__file__).parent.resolve().__str__()
    check_output(path + "/../../mmt/MultiMonitorTool.exe /stext temp", shell=True)
    try:
        with open("temp", 'r', encoding=get_encoding_type("temp")) as f, open("trgfile", 'w', encoding='utf-8') as e:
            text = f.read()
            e.write(text)

        os.remove("temp")
        os.rename("trgfile", "temp")
    except UnicodeDecodeError:
        print('Decode Error')
    except UnicodeEncodeError:
        print('Encode Error')

    didLine = linecache.getline('temp', 14)
    dName = ""
    if "usbmmidd" in didLine:
        dName = linecache.getline('temp', 12).split(".")[1]

    os.remove("temp")
    return dName