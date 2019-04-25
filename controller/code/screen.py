"""
Class for displaying on the screen
"""
from PIL import ImageFont, ImageDraw
import time
from luma.core.interface.serial import i2c, spi
from luma.core.render import canvas
from luma.oled.device import ssd1306

class Screen():
    def __init____(self):
        self._serial = spi(device=0, port=0)
        self._device = ssd1306(self._serial, rotate=2)

    def clockScreen(self):
        pass

    # alarmScreen handels the graphichs of viewing, setting and activating alarms
    # uses external functions to achieve this
    def alarmScreen(self, alarms):
        fontSize = 17
        blockSize = 22

        for alarm in alarms:
            for Y in range(64):
                    self.drawAlarm(alarm, Y, fontSize, blockSize)
                    time.sleep(0.015)


    # settingsScreen handels the graphichs of the settings screen. Similar to alarmScreen.
    def settingsScreen(self):
        pass


    def drawAlarm(alarm, fontSize, blockSize):
        alarmTime = str(alarm)
        alarmAuto = False
        alarmActive = alarm.isActivated()
        W = 128
        H = 64
        fontBold = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf", fontSize)
        font = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeMono.ttf", fontSize)
        if alarmActive:
                activeColor = "white"
        else:
                activeColor = "black"

        if alarmAuto:
                autoStr = "cal"
        else:
                autoStr = "man"
        with canvas(self._device) as draw:
                draw.line((0, Y, W, Y), fill="white")
                draw.line((0, Y+blockSize, W, Y+blockSize), fill="white")
                draw.text((0, Y+(blockSize-fontSize)/2), alarmTime, fill="white", font=fontBold)
                autoStrSize = draw.textsize(autoStr, font=font)
                draw.text((W-blockSize-autoStrSize[0], Y+(blockSize-fontSize)/2), autoStr, fill="white")
                draw.ellipse((W-blockSize+9, Y+5, W-1, Y+blockSize-5), outline="white", fill=activeColor)
