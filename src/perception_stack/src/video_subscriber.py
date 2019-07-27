#!/usr/bin/env python
import rospy
import cv2
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

def img_cb(msg):
    #convert msg to cv2 message
    try:
        cvimage = CvBridge().imgmsg_to_cv2(msg,desired_encoding="passthrough")
        cv2.imshow("subscribed",cvimage)
        cv2.waitKey(1)
    except CvBridgeError as e:
        print(e)

rospy.init_node("image_getter",anonymous=True)
image_sub = rospy.Subscriber('/android_image',Image,img_cb)
rospy.spin()
