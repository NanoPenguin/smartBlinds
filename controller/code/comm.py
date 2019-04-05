"""
Class for communication with blinds-unit

Method: https://oscarliang.com/raspberry-pi-arduino-connected-i2c/
"""

import smbus

class Comm():
    def __init__(self):
        self.__bus = smbus.SMBus(0)
        self.__address = 0x04


    def write(self, data):
        self.__bus.write_byte(self._address, data)


    def read(self):
        data = self.__bus.read_byte(self.__address)
