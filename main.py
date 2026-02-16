import os 
import eel

from engine.features import *
from engine.command import *
from engine.auth import recoganize

def start():

    eel.init("www")

    playAssistantsound()   
    @eel.expose
    def init():
        #subprocess.call(['device.bat'])
        eel.hideLoader()
        speak("ready for face Authentication")
        flag = recoganize.AuthenticateFace()
        if flag ==1:
             eel.hideFaceAuth()
             speak(" Face Authentication Successful")
             eel.hideFaceAuthSuccess()
             speak(" Hello, Welcome sir,how can i Help you")
             eel.hideStart()
             playAssistantsound()
        else:
             speak("Face Authentication fail")
    os.system('start msedge.exe --app="http://localhost:8000/index.html"')

    eel.start('intex.html', mode=None, host='localhost', block=True)


