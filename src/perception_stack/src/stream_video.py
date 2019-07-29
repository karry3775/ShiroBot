#!/usr/bin/env python
import rospy
import numpy as np
import cv2
import urllib as ul
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
"""
TASKS
1. get video stream from the android phone
2. do perspective transform and publish that image to /android_image topic
"""
url ="http://192.168.0.2:8080/shot.jpg" #this url you can get from the IP Webcam
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
    #lets do the perpective transformation now
    pts1 = np.float32([[320,70],[927,93],[105,630],[1105,650]])
    # pts2 = np.float32([[0,0],[600,0],[0,400],[600,400]])
    """
    Before calculating new image dimensions need to find out
    the max width and max height
    """
    w1 = 927 - 320
    w2 = 1105 - 105
    h1 = 630 - 70
    h2 = 650 - 93
    maxw = max(w1,w2)
    maxh = max(h1,h2)
    pts2 = np.float32([[0,0],[maxw,0],[0,maxh],[maxw,maxh]])
    matrix = cv2.getPerspectiveTransform(pts1,pts2)

    # result = cv2.warpPerspective(imgcv,matrix,(600,400))
    result = cv2.warpPerspective(imgcv,matrix,(maxw,maxh))
    try:
        msg_to_publish = CvBridge().cv2_to_imgmsg(result)
        pub.publish(msg_to_publish)
    except CvBridgeError as e:
        print(e)
    if ord('q')==cv2.waitKey(1) & 0xFF:
        exit(0)


cv2.destroyAllWindows()
