#https://forum.arduino.cc/index.php?topic=225329.msg1810764#msg1810764
"""
Class for communication between RPi and Arduino via Serial
"""

import serial
from time import sleep

startMarker = 60
endMarker = 62


class Communication():
  def __init__(self, serPort = "/dev/ttyUSB0" , baudRate = 9600):
    self._setpoint = 0
    self._serPort = serPort
    self._baudRate = baudRate
    self._ser = self.startSerial(self._serPort, self._baudRate)
    try:
      self.waitForArduino()
    except AttributeError:
      pass


  # destructor
  def __del__(self):
    try:
        self._ser.close
    except AttributeError:
      pass


  # start a serial connection
  def startSerial(self, serPort, baudRate):
    try:
      ser = serial.Serial(serPort, baudRate)
      return ser
    except serial.SerialException:
      print("Could not start serial connection")


  # send string to arduino
  def sendToArduino(self, sendStr):
    self._ser.write(sendStr.encode())


  # recieve string from arduino
  def recvFromArduino(self):
    global startMarker, endMarker
    ck = ""
    x = "z" # any value that is not an end- or startMarker
    byteCount = -1 # to allow for the fact that the last increment will be one too many
    # wait for the start character
    while  ord(x) != startMarker:
      x = self._ser.read()
    # save data until the end marker is found
    while ord(x) != endMarker:
      if ord(x) != startMarker:
        ck = ck + x.decode()
        byteCount += 1
      x = self._ser.read()
    return(ck)


  # wait until the Arduino sends 'Arduino Ready' - allows time for Arduino reset
  # it also ensures that any bytes left over from a previous message are discarded
  def waitForArduino(self):
      global startMarker, endMarker
      msg = ""
      while msg.find("Arduino is ready") == -1:
        while self._ser.inWaiting() == 0:
          pass
        msg = self.recvFromArduino()


  # tell arduino to set blinds to scpecifik angle
  def setBlinds(self, setpoint, time_ = 0):
      # Fully open setpoint 600
      # For smoth recursive calling jump setps of 20
      waitingForReply = False
      n = 0
      commandstr = "#<" + "setBlinds,2," + str(setpoint) + "," + str(time_) + ">"
      if waitingForReply == False:
        self.sendToArduino(commandstr)
        waitingForReply = True
      sleep(0.1)


  # get current blinds angle
  def getBlindsData(self):
    waitingForReply = False
    n = 0
    commandstr = "#<" + "getBlinds,0" + ">"
    if waitingForReply == False:
        self.sendToArduino(commandstr)
        waitingForReply = True
    if waitingForReply == True:
        while self._ser.inWaiting() == 0:
          pass
        dataRecvd = self.recvFromArduino()
        n += 1
        waitingForReply = False
        sleep(0.1)
        setpointOnArduino, feedbackPotOnArduino = self.parseresponse(dataRecvd)
        return setpointOnArduino, feedbackPotOnArduino


  # split up the response
  def parseresponse(self, data):
      data = data.split(" ")
      setpointOnArduino = data[1]
      feedbackPotOnArduino = data[3]
      return int(setpointOnArduino), int(feedbackPotOnArduino)
