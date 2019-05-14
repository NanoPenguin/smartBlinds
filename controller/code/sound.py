from time import sleep
import RPi.GPIO as GPIO

SPEAKER_PIN = 13

class Sound():
    def __init__(self):
        global SPEAKER_PIN
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(SPEAKER_PIN, GPIO.OUT)
        self._lastSwitch = 0
        self._soundOn = False


    def beep(self,beepLength):
        millis = int(round(time.time() * 1000))
        timeSinceLast = millis-self._lastSwitch
        #print(str(timeSinceLast)+' sinceLast')
        #print(str(beepLength*1000) +' beeplength')
        if self._soundOn:
            if(timeSinceLast>beepLength*1000):
                self.stop()
                self._soundOn = False
                self._lastSwitch = millis
        else:
            if(millis-self._lastSwitch>beepLength*1000):
                self.IO.digitalWrite(SPEAKER_PIN,'HIGH')
                self._soundOn = True
                self._lastSwitch = millis


    def stop(self):
        GPIO.output(SPEAKER_PIN,GPIO.LOW)
