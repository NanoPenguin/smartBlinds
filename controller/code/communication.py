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

  def __del__(self): # Destructor
    try:
        self._ser.close
    except AttributeError:
      pass

  def startSerial(self, serPort, baudRate):
    try:
      ser = serial.Serial(serPort, baudRate)
      #DEBUG: print("Serial port " + serPort + " opened  Baudrate " + str(baudRate))

      return ser

    except serial.SerialException:
      print("Could not start serial connection")

  def sendToArduino(self, sendStr):
    self._ser.write(sendStr.encode())

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

  def waitForArduino(self):

    # wait until the Arduino sends 'Arduino Ready' - allows time for Arduino reset
    # it also ensures that any bytes left over from a previous message are discarded

      global startMarker, endMarker

      msg = ""
      while msg.find("Arduino is ready") == -1:

        while self._ser.inWaiting() == 0:
          pass

        msg = self.recvFromArduino()

        # Debug: print(msg)
        # print

  def setBlinds(self, setpoint):
      # Fully open setpoint 600
      # For smoth recursive calling jump setps of 20
      waitingForReply = False
      n = 0
      commandstr = "<" + "setBlinds,1," + str(setpoint) + ">"

      if waitingForReply == False:
        self.sendToArduino(commandstr)
        #print "Sent from PC -- LOOP NUM " + str(n) + " TEST STR " + str(commandstr)
        waitingForReply = True

      #print "==========="

      sleep(0.1)

  def getBlindsData(self):
    waitingForReply = False
    n = 0
    commandstr = "<" + "getBlinds,0" + ">"

    if waitingForReply == False:
        self.sendToArduino(commandstr)
        #print "Sent from PC -- LOOP NUM " + str(n) + " TEST STR " + str(commandstr)
        waitingForReply = True

    if waitingForReply == True:

        while self._ser.inWaiting() == 0:
          pass

        dataRecvd = self.recvFromArduino()
        #print "Reply Received  " + dataRecvd
        n += 1
        waitingForReply = False

      # print "==========="

        sleep(0.1)

        setpointOnArduino, feedbackPotOnArduino = self.parseresponse(dataRecvd)

        return setpointOnArduino, feedbackPotOnArduino

  def parseresponse(self, data):
      data = data.split(" ")
      setpointOnArduino = data[1]
      feedbackPotOnArduino = data[3]
      return int(setpointOnArduino), int(feedbackPotOnArduino)
