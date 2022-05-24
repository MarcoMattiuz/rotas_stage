import os
import eel
from win32api import GetSystemMetrics
# non funziona su linux


absolutepath = os.path.abspath(__file__)
absolutepath = absolutepath[0:-6] + "web"
eel.init(absolutepath)


@eel.expose
def start():
    eel.prompt_alerts('MQTT started')


eel.start('index.html',
          size=(GetSystemMetrics(0)-200, GetSystemMetrics(1)-200),
          position=(100, 100))
