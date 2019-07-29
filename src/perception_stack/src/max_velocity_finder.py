#!/usr/bin/env python
import rospy
from perception_stack.msg import state_msg
import numpy as np
import time
import matplotlib.pyplot as plt

"""
TASKS
1. subscibe to the topic /shiro_state and display the states
2. put all the states in a global state value
"""
global statex
statex = []
statey = []

def state_cb(msg):
    global state
    data = msg.data
    time_stamp = data[0]
    x = data[1]
    y = data[2]
    theta = data[3]
    print("Time: {}, x: {}, y: {}, theta: {}".format(time_stamp,x,y,theta))
    statex.append(x)
    statey.append(y)

rospy.init_node('max_vel_finder_node')
state_sub = rospy.Subscriber('/shiro_state', state_msg, state_cb)
rospy.spin()

#use the global state variable to obtain the graph
# state = np.array(state)
print(statex)
print(statey)
plt.plot(statex,statey,label='path')
plt.legend()
plt.show()
