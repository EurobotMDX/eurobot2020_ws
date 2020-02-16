#!/usr/bin/env python

port = "/dev/serial/by-path/platform-xhci-hcd.3.auto-usb-0:1.2:1.0-port0"
baud = 230400

import serial
import time
import signal

s = serial.Serial(port, baud, timeout=1)

try:
	print ("\nctrl-c to terminate\n")
	while True:
		if s.in_waiting > 0:
			print ("Buffer contains {data}".format(data=s.read(s.in_waiting)))
		time.sleep(0.1)
except KeyboardInterrupt:
	pass

print ("\nTerminating ....")
s.close()
