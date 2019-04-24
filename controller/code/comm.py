"""
Class for communication with blinds-unit

Method: https://oscarliang.com/raspberry-pi-arduino-connected-i2c/
"""

import smbus

class Comm():
    # initialize I2C
    def __init__(self):
        self.__bus = smbus.SMBus(0)
        self.__address = 0x04


    # writes 1 byte of data
    def write(self, data):
        self.__bus.write_byte(self._address, data)

    # reads one byte of data
    def read(self):
        data = self.__bus.read_byte(self.__address)
