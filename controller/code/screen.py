"""
Class for displaying on the screen
"""

import time
from PIL import ImageFont, ImageDraw
from luma.core.interface.serial import i2c, spi
from luma.core.render import canvas
from luma.oled.device import ssd1306

SCREENSERIAL = spi(device=0, port=0)
SCREENDEVICE = ssd1306(SCREENSERIAL, rotate=2)


class Screen():
    def __init__(self, alarms):
        self._scrollIndex = 0
        self._currentScroll = 0
        self._scrollDelay = 0
        self._alarms = alarms

    def clockScreen(self):
        pass

    # alarmScreen handels the graphichs of viewing, setting and activating alarms
    # uses external functions to achieve this
    def alarmScreen(self):
        fontSize = 17
        blockSize = 22

        W = 128
        H = 64
        fontBold = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf", fontSize)
        font = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeMono.ttf", fontSize)
        if self._currentScroll < self._scrollIndex:
            scrollDirUp = False
        else:
            scrollDirUp = True
        for animationConst in range(blockSize,-1,-2):
            if scrollDirUp:
                #animationConst = blockSize - animationConst
                animationConst = -animationConst
            with canvas(SCREENDEVICE) as draw:
                for alarm in self._alarms:
                    alarmTime = str(alarm)
                    alarmAuto = alarm.isFromCalendar()
                    alarmActive = alarm.isActivated()
                    if alarmActive:
                            activeColor = "white"
                    else:
                            activeColor = "black"

                    if alarmAuto:
                            autoStr = "cal"
                    else:
                            autoStr = "man"
                    Y = (self._alarms.index(alarm)-self._currentScroll) * blockSize + animationConst - 1
                    if self._currentScroll == self._scrollIndex:
                            Y += blockSize*2
                    else:
                        if scrollDirUp:
                            Y += blockSize*2
                    #print('index: {}  scroll: {}  animationConst: {}  Y: {}'.format(self._alarms.index(alarm), self._currentScroll, animationConst, Y))
                    draw.line((0, Y, W, Y), fill="white")
                    draw.line((0, Y+blockSize, W, Y+blockSize), fill="white")
                    draw.text((4, Y+(blockSize-fontSize)/2), alarmTime, fill="white", font=fontBold)
                    autoStrSize = draw.textsize(autoStr, font=font)
                    draw.text((W-blockSize-autoStrSize[0], Y+(blockSize-fontSize)/2), autoStr, fill="white", font=font)
                    draw.ellipse((W-blockSize+9, Y+5, W-1, Y+blockSize-5), outline="white", fill=activeColor)
                    draw.rectangle((0, blockSize, 2, blockSize*2-1), fill="white")
                if self._currentScroll == self._scrollIndex:
                    break
            time.sleep(self._scrollDelay)
        self._currentScroll = self._scrollIndex


    def alarmScrollDown(self):  # scrolls and selects next alarm
        self._scrollIndex+=1
        self.alarmScreen()


    def alarmScrollUp(self):  # scrolls and selects previous alarm
        if self._scrollIndex:
            self._scrollIndex-=1
        self.alarmScreen()


    def selectedAlarm(self):  # returns the selected alarm
        return self._alarms[self._currentScroll]


    # settingsScreen handels the graphichs of the settings screen. Similar to alarmScreen.
    def settingsScreen(self):
        pass
