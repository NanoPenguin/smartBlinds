from time import sleep
from gpio import *

SPEAKER_PIN = 13

class Sound():
    def __init__(self,io):
        self.IO = io
        self._lastSwitch = 0
        self._soundOn = False


    def beep(self,beepLength):
        millis = int(round(time.time() * 1000))
        print(str(millis-self._lastSwitch)+' sinceLast')
        print(str(beepLength*1000) +' beeplength')
        if self._soundOn:
            self.IO.digitalWrite(SPEAKER_PIN,'HIGH')
            if(millis-self._lastSwitch>beepLength*1000):
                self.stop()
                self._soundOn = False
                self._lastSwitch = millis
        else:
            self.stop()
            if(millis-self._lastSwitch>beepLength*1000):
                self.IO.digitalWrite(SPEAKER_PIN,'HIGH')
                self._soundOn = True
                self._lastSwitch = millis


    def stop(self):
        self.IO.digitalWrite(SPEAKER_PIN,'LOW')
