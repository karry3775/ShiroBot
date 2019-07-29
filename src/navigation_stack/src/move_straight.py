#!/usr/bin/env python
import numpy as np
import socket
import time

"""
TASKS FOR THIS NODE
send user define w commands to robot
"""


HOST = '192.168.43.250'  # The server's name for the ESP8266 Wifi
PORT = 80        # The port used by the server
s = socket.socket()
s.connect((HOST,PORT))
text = str(150) + ':' + str(100) + 'n ' + '\n'
s.send(text.encode('utf-8'))
print(100,100,text)
time.sleep(5)
s.send(b'0:0n \n')
print(0,0)
data = s.recv(10)
s.close()
