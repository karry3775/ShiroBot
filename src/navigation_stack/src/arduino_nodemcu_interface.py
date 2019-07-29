#!/usr/bin/env python
import rospy
from navigation_stack.msg import control_msg
import numpy as np
import socket
import time
import argparse

"""
TASKS FOR THIS NODE
1. Listen to any higher level commands on v and w values (subscribe to some topic)
2. Convert them to appropriate wL and wR commands
3. send them thats it
"""
def wrapTolimits(w):
    if w>255:
        w = 255
    if w< -255:
        w = -255
    return w

def cmd_cb(msg):
    v = msg.data[0]
    w = msg.data[1]
    #convert them to apt wL anf wR commands
    b = 0.125
    r = 0.034
    wL = (2*v - w*b)/(2*r)
    wR = (2*v + w*b)/(2*r)

    print(wL,wR)
    #map them to arduino inputs
    wL_new = wrapTolimits(177.5735 - 21.8769*abs(wL) + 1.603*(wL**2))
    wR_new = wrapTolimits(177.5735 - 21.8769*abs(wR) + 1.603*(wR**2))

    if wL < 0 :
        wL_new = -wL_new
    else:
        pass
    if wR < 0:
        wR_new = -wR_new
    else:
        pass

    try:
        text = str(wL_new) + ':' + str(wR_new) + 'n ' + '\n'
        s.send(text.encode('utf-8'))
        print(wL_new,wR_new,text)
        time.sleep(1)

    except KeyboardInterrupt:
        s.send(b'0:0n \n')
        print(0,0)

    s.send(b'0:0n \n')
    data = s.recv(10)
    s.close()


HOST = '192.168.43.250'  # The server's name for the ESP8266 Wifi
PORT = 80        # The port used by the server
s = socket.socket()
s.connect((HOST,PORT))

rospy.init_node('arduino_nodemcu_interface_node')
cmd_sub = rospy.Subscriber('/hl_commands',control_msg, cmd_cb) #this stands for higher level commands
rospy.spin()
