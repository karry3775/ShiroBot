#!/usr/bin/env python
import rospy
from navigation_stack.msg import control_msg
import numpy as np
"""
Tasks:
1. To send high level commands as obtained from planner/ controller
2. For testing send commands from terminal
"""

rospy.init_node('hl_cmd_pub_node')
cmd_pub = rospy.Publisher('/hl_commands', control_msg, queue_size = 10)
rate = rospy.Rate(10) #10 hertz
cmd = control_msg()

while not rospy.is_shutdown():
    v = 1.5
    w = 0
    cmd.data = [float(v),float(w)]
    cmd_pub.publish(cmd)
    rate.sleep()
