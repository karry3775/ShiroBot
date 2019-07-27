#!/usr/bin/env python
import rospy
import numpy as np
import cv2
import urllib as ul
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

url ="http://192.168.0.7:8080/shot.jpg" #this url you can get from the IP Webcam
#create a publisher
rospy.init_node("android_image_node",anonymous=True)
pub = rospy.Publisher("/android_image",Image,queue_size=10)


while not rospy.is_shutdown():
    #getting the reponse
    resp = ul.urlopen(url)
    #converting the numpy image
    imgnp = np.array(bytearray(resp.read()),dtype='uint8')
    #converting to opencv image
    imgcv = cv2.imdecode(imgnp,-1)
    #display image
    # cv2.imshow('mobile_feed',imgcv)
    try:
        msg_to_publish = CvBridge().cv2_to_imgmsg(imgcv)
        pub.publish(msg_to_publish)
    except CvBridgeError as e:
        print(e)
    if ord('q')==cv2.waitKey(1) & 0xFF:
        exit(0)


cv2.destroyAllWindows()
