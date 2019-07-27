#!/usr/bin/env python
import rospy
import cv2
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
from cv2 import aruco
import numpy as np

def img_cb(msg):
    #convert msg to cv2 message
    try:
        frame = CvBridge().imgmsg_to_cv2(msg,desired_encoding="passthrough")
        cv2.imshow("subscribed",frame)

        #aruco_detection starts here
        gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
        params = aruco.DetectorParameters_create()

        corners, ids, rejectedImgPoints = aruco.detectMarkers(gray,aruco_dict,parameters=params)
        #find (x,y,theta)
        if corners:
            corner_array = np.reshape(np.array(corners),(4,2))
            a = corner_array[0,:]
            b = corner_array[1,:]
            c = corner_array[2,:]
            d = corner_array[3,:]
            centerx = int((a[0] + b[0] + c[0] + d[0])/4)
            centery = int((a[1] + b[1] + c[1] + d[1])/4)
            axisy_x = int((a[0] + b[0])/2)
            axisy_y = int((a[1] + b[1])/2)
            axisx_x = int((b[0] + c[0])/2)
            axisx_y = int((b[1] + c[1])/2)

            cv2.circle(frame,(a[0],a[1]),10,(0,0,255),-1)
            cv2.circle(frame,(b[0],b[1]),10,(255,0,0),-1)
            cv2.circle(frame,(c[0],c[1]),10,(0,255,0),-1)
            cv2.circle(frame,(d[0],d[1]),10,(0,0,0),-1)
            cv2.circle(frame,(centerx,centery),10,(255,255,0),-1)

            #drawing axes
            cv2.line(frame,(centerx,centery),(axisy_x,axisy_y),(255,0,0),5)
            cv2.line(frame,(centerx,centery),(axisx_x,axisx_y),(0,255,0),5)

        frame = aruco.drawDetectedMarkers(frame,corners)
        cv2.imshow('frame',frame)

        cv2.waitKey(1)
    except CvBridgeError as e:
        print(e)

rospy.init_node("image_getter",anonymous=True)
image_sub = rospy.Subscriber('/android_image',Image,img_cb)
rospy.spin()
