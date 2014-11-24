#!/usr/bin/python2
import serial
import re, sys, signal, os, time, datetime
import serial.tools.list_ports

BITRATE = 19200

class RFID():
  def get_ports(self):
    com_ports = set()
    try:
      for port, desc, port_type in serial.tools.list_ports.comports():
	    #print port
        com_ports.add(port)
    except:
      pass
    return com_ports  
	
  def connect(self, port):
    self.ser = serial.Serial(port, BITRATE, timeout=0)

  def signal_handler(self, signal, frame):
    print "Closing RFID reader"
    if (self.ser != None):
      self.ser.fser.close()
    sys.exit(0)
  
  def read_from_serial(self):
    buffer = ''
    rfidPattern = re.compile(b'[\W_]+')
    signal.signal(signal.SIGINT, self.signal_handler)
 
    while True:
      # Read data from RFID reader
      buffer = buffer + self.ser.read(self.ser.inWaiting())
      if len(buffer) > 10:
        #lines = buffer.split('\n')
        last_received = buffer[:10]
        # Clear buffer
        buffer = ''
        lines = ''
        return last_received

      time.sleep(0.1)

