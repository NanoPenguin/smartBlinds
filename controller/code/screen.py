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
    def __init__(self, alarms, settingsObject):
        self._scrollIndex = 0
        self._currentScroll = 0
        self._scrollDelay = 0
        self._alarms = alarms
        self._settingsObject = settingsObject
        self._blockSize = 22
        self._fontSize = 17
        self._fontName = "FreeMono.ttf"
        self._fontNameBold = "FreeMonoBold.ttf"
        self._fontLocation = "/usr/share/fonts/truetype/freefont/"
        self._fontBold = ImageFont.truetype(self._fontLocation + self._fontNameBold, self._fontSize)
        self._font = ImageFont.truetype(self._fontLocation + self._fontName, self._fontSize)
        self._clockFontSize = 30
        self._fontClock = ImageFont.truetype(self._fontLocation + self._fontNameBold, self._clockFontSize)
        self._lastMode = ''


    def messageScreen(self, message):
        W = 128
        H = 64
        with canvas(SCREENDEVICE) as draw:
            Y = int(H/2-self._fontSize/2-(len(message)-1)*(self._fontSize+2)/2)
            for line in message:
                draw.text((4, Y), line, fill="white", font=self._font)
                Y += self._fontSize


    def clockScreen(self):
        W = 128
        H = 64
        earliest = 0
        earliestAlarm = ''
        if self._alarms:
            for alarm in self._alarms:
                if alarm. isActivated():
                    earliest = alarm.getTime()
                    earliestAlarm = alarm
                    break
        for alarm in self._alarms:
            tempTime = alarm.getTime()
            if tempTime < earliest and alarm.isActivated():
                earliest = tempTime
                earliestAlarm = alarm
        timeStr = time.strftime('%H:%M', time.localtime(time.time()))
        with canvas(SCREENDEVICE) as draw:
            w, h = draw.textsize(timeStr, font=self._fontClock)
            draw.text(((W-w)/2, (H-h)/2), timeStr, fill="white", font=self._fontClock)
            if earliest:
                draw.text((0, H-self._fontSize), str(earliestAlarm), fill="white", font=self._font)
        self._lastMode = 'clock'


    # alarmScreen handels the graphichs of viewing, setting and activating alarms
    # uses external functions to achieve this
    def alarmScreen(self):
        if self._lastMode != 'alarm':
            self.resetScroll()
        newAlarm = 'New Alarm'
        updateCalAlarms = 'Update cal.'
        alarms = list(self._alarms)
        alarms.append(newAlarm)
        alarms.append(updateCalAlarms)
        W = 128
        H = 64
        if self._currentScroll < self._scrollIndex:
            scrollDirUp = False
        else:
            scrollDirUp = True
        for animationConst in range(self._blockSize,-1,-2):
            if scrollDirUp:
                #animationConst = self._blockSize - animationConst
                animationConst = -animationConst
            with canvas(SCREENDEVICE) as draw:
                for alarm in alarms:
                    #print(alarm)
                    if alarms.index(alarm) <= self._scrollIndex+2 and \
                        alarms.index(alarm) >= self._scrollIndex-2:
                        if alarm not in [newAlarm, updateCalAlarms]:
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
                                    autoStr = ""
                        Y = (alarms.index(alarm)-self._currentScroll) * self._blockSize + animationConst - 1
                        #print(Y)
                        if self._currentScroll == self._scrollIndex:
                                Y += self._blockSize*2
                        else:
                            if scrollDirUp:
                                Y += self._blockSize*2
                        draw.line((0, Y, W, Y), fill="white")
                        #draw.line((0, Y+self._blockSize, W, Y+self._blockSize), fill="white")
                        draw.rectangle((0, self._blockSize, 2, self._blockSize*2-1), fill="white")
                        if alarm not in [newAlarm, updateCalAlarms]:
                            draw.text((4, Y+(self._blockSize-self._fontSize)/2), alarmTime, fill="white", font=self._fontBold)
                            autoStrSize = draw.textsize(autoStr, font=self._font)
                            draw.text((W-self._blockSize-autoStrSize[0], Y+(self._blockSize-self._fontSize)/2), autoStr, fill="white", font=self._font)
                            draw.ellipse((W-self._blockSize+9, Y+5, W-1, Y+self._blockSize-5), outline="white", fill=activeColor)
                        elif alarm == newAlarm:
                            draw.text((4, Y+(self._blockSize-self._fontSize)/2), newAlarm, fill="white", font=self._font)
                        else:
                            draw.text((4, Y+(self._blockSize-self._fontSize)/2), updateCalAlarms, fill="white", font=self._font)
                if self._currentScroll == self._scrollIndex:
                    break
            time.sleep(self._scrollDelay)
        self._currentScroll = self._scrollIndex
        self._lastMode = 'alarm'


    def scrollDown(self):  # scrolls and selects next alarm
        if self._lastMode == 'alarm':
            if len(self._alarms)+1 > self._currentScroll:
                self._scrollIndex+=1
            self.alarmScreen()
        elif self._lastMode == 'settings':
            if len(self._settingsObject.getKeys()) > self._currentScroll+1:
                self._scrollIndex+=1
            self.settingsScreen()


    def scrollUp(self):  # scrolls and selects previous alarm
        if self._scrollIndex:
            self._scrollIndex-=1
        if self._lastMode == 'alarm':
            self.alarmScreen()
        elif self._lastMode == 'settings':
            self.settingsScreen()


    def selectedAlarm(self):  # returns the selected alarm
        if len(self._alarms) > self._currentScroll:
            return self._alarms[self._currentScroll]
        elif len(self._alarms) == self._currentScroll:
            return 'newAlarm'
        else:
            return 'updateCalAlarms'


    def selectedSetting(self):  # returns the selected setting
        keys = [key for key in self._settingsObject.getKeys()]
        if len(keys) > self._currentScroll:
            return keys[self._currentScroll]
        else:
            return False


    def setHourScreen(self, timeStr):
        timeList = timeStr.split(':')
        W = 128
        H = 64
        Ycal = 2
        with canvas(SCREENDEVICE) as draw:
            w, h = draw.textsize(':', font=self._fontClock)
            draw.text(((W-w)/2, (H-h)/2), ':', fill="white", font=self._fontClock)
            w, h = draw.textsize(timeList[0], font=self._fontClock)
            draw.rectangle(((W/2-w)/2, (H-h)/2+Ycal, (W/2-w)/2+w, (H-h)/2+h+Ycal), fill="white")
            draw.text(((W/2-w)/2, (H-h)/2), timeList[0], fill="black", font=self._fontClock)
            w, h = draw.textsize(timeList[1], font=self._fontClock)
            draw.text(((W/2-w)/2+W/2, (H-h)/2), timeList[1], fill="white", font=self._fontClock)


    def setMinuteScreen(self, timeStr):
        timeList = timeStr.split(':')
        W = 128
        H = 64
        Ycal = 2
        with canvas(SCREENDEVICE) as draw:
            w, h = draw.textsize(':', font=self._fontClock)
            draw.text(((W-w)/2, (H-h)/2), ':', fill="white", font=self._fontClock)
            w, h = draw.textsize(timeList[0], font=self._fontClock)
            draw.rectangle(((W/2-w)/2+W/2, (H-h)/2+Ycal, (W/2-w)/2+w+W/2, (H-h)/2+h+Ycal), fill="white")
            draw.text(((W/2-w)/2, (H-h)/2), timeList[0], fill="white", font=self._fontClock)
            w, h = draw.textsize(timeList[1], font=self._fontClock)
            draw.text(((W/2-w)/2+W/2, (H-h)/2), timeList[1], fill="black", font=self._fontClock)


    # settingsScreen handels the graphichs of the settings screen. Similar to alarmScreen.
    def settingsScreen(self):
        if self._lastMode != 'settings':
            self.resetScroll()
        W = 128
        H = 64
        if self._currentScroll < self._scrollIndex:
            scrollDirUp = False
        else:
            scrollDirUp = True
        keys = self._settingsObject.getKeys()
        print
        for animationConst in range(self._blockSize,-1,-2):
            if scrollDirUp:
                #animationConst = self._blockSize - animationConst
                animationConst = -animationConst
            with canvas(SCREENDEVICE) as draw:
                for key in keys:
                    if keys.index(key) <= self._scrollIndex+2 and \
                        keys.index(key) >= self._scrollIndex-2:
                        Y = (keys.index(key)-self._currentScroll) * self._blockSize + animationConst - 1
                        if self._currentScroll == self._scrollIndex:
                                Y += self._blockSize*2
                        else:
                            if scrollDirUp:
                                Y += self._blockSize*2
                        draw.line((0, Y, W, Y), fill="white")
                        #draw.line((0, Y+self._blockSize, W, Y+self._blockSize), fill="white")
                        draw.rectangle((0, self._blockSize, 2, self._blockSize*2-1), fill="white")
                        draw.text((4, Y+(self._blockSize-self._fontSize)/2), key, fill="white", font=self._font)
                if self._currentScroll == self._scrollIndex:
                    break
            time.sleep(self._scrollDelay)
        self._currentScroll = self._scrollIndex
        self._lastMode = 'settings'


    def resetScroll(self):
        self._currentScroll = 0
        self._scrollIndex = 0
