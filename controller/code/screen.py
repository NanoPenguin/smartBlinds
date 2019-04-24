"""
Class for displaying on the screen
"""
"""
from luma.core.interface.serial import i2c, spi
from luma.core.render import canvas
from luma.oled.device import ssd1306, ssd1309, ssd1325, ssd1331, sh1106
"""
class Screen():
    def __init____(self):
        self._serial = spi(device=0, port=0)
        self._screen = ssd1306(self._serial)

    def clockScreen(self):
        pass

    # alarmScreen handels the graphichs of viewing, setting and activating alarms
    # uses external functions to achive this
    def alarmScreen(self):
        pass

    # settingsScreen handels the graphichs of the settings screen. Similar to alarmScreen.
    def settingsScreen(self):
        pass
