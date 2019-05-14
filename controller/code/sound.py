from time import sleep
from gpio import *

SPEAKER_PIN = 13

class Sound():
    def __init__(self,IO):
        self.IO = IO
        self._lastSwitch = 0
        self._soundOn = False


    def beep(self,beepLength):
        millis = int(round(time.time() * 1000))
        print(millis-self._lastSwitch+' sinceLast')
        print(beepLength*1000 +' beeplength')
        if(millis-self._lastSwitch>beepLength*1000):
            if self._soundOn:
                self.stop()
                self._soundOn = False
                self._lastSwitch = millis
            else:
                self.IO.digitalWrite(SPEAKER_PIN,'HIGH')
                self._soundOn = True
                self._lastSwitch = millis


    def stop(self):
        self.IO.digitalWrite(SPEAKER_PIN,'LOW')
