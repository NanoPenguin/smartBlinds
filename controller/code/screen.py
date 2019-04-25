"""
Class for displaying on the screen
"""
from PIL import ImageFont, ImageDraw
from luma.core.interface.serial import i2c, spi
from luma.core.render import canvas
from luma.oled.device import ssd1306

SCREENSERIAL = spi(device=0, port=0)
SCREENDEVICE = ssd1306(SCREENSERIAL, rotate=2)


class Screen():
    def __init__(self):
        self._scrollIndex = 0
        self._currentScroll = 0
        self._scrollDelay = 0.02

    def clockScreen(self):
        pass

    # alarmScreen handels the graphichs of viewing, setting and activating alarms
    # uses external functions to achieve this
    def alarmScreen(self, alarms):
        fontSize = 17
        blockSize = 22

        W = 128
        H = 64
        fontBold = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf", fontSize)
        font = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeMono.ttf", fontSize)
        while(self._scrollIndex!=self._currentScroll):
            with canvas(SCREENDEVICE) as draw:
                for alarm in alarms:
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
                    Y = (alarms.index(alarm)+1-self._currentScroll) * blockSize
                    draw.line((0, Y, W, Y), fill="white")
                    draw.line((0, Y+blockSize, W, Y+blockSize), fill="white")
                    draw.text((0, Y+(blockSize-fontSize)/2), alarmTime, fill="white", font=fontBold)
                    autoStrSize = draw.textsize(autoStr, font=font)
                    draw.text((W-blockSize-autoStrSize[0], Y+(blockSize-fontSize)/2), autoStr, fill="white", font=font)
                    draw.ellipse((W-blockSize+9, Y+5, W-1, Y+blockSize-5), outline="white", fill=activeColor)
        if self._scrollIndex > self._currentScroll:
            self._currentScroll += self._scrollDelay
        else:
            self._currentScroll -= self._scrollDelay
        time.sleep(0.05)


    def scrollDown(self):
        self._scrollIndex+=1


    def scrollUp(self):
        if self._scrollIndex:
            self._scrollIndex-=1


    # settingsScreen handels the graphichs of the settings screen. Similar to alarmScreen.
    def settingsScreen(self):
        pass
