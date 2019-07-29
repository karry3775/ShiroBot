#!/usr/bin/env python
import rospy
import cv2
from sensor_msgs.msg import Image
from perception_stack.msg import state_msg
from cv_bridge import CvBridge, CvBridgeError
from cv2 import aruco
import numpy as np
import math as m
import time

tic = time.time()

def change_pt(a):
    y = a[1]
    y_new = 560 - y
    a[1] = y_new
    return a

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
            axisy_x = int((c[0] + d[0])/2)
            axisy_y = int((c[1] + d[1])/2)
            axisx_x = int((a[0] + d[0])/2)
            axisx_y = int((a[1] + d[1])/2)

            cv2.circle(frame,(a[0],a[1]),10,(0,0,255),-1) #a is red
            cv2.circle(frame,(b[0],b[1]),10,(255,0,0),-1) #b is blue
            cv2.circle(frame,(c[0],c[1]),10,(0,255,0),-1) #c is green
            cv2.circle(frame,(d[0],d[1]),10,(0,0,0),-1) #d is black
            #lets calculate theta
            a = change_pt(a)
            b = change_pt(b)
            theta = m.degrees(m.atan2((a[1]-b[1]),(a[0]-b[0])))
            cv2.circle(frame,(centerx,centery),2,(255,255,0),-1)

            #drawing axes
            cv2.line(frame,(centerx,centery),(axisy_x,axisy_y),(255,0,0),5)
            cv2.line(frame,(centerx,centery),(axisx_x,axisx_y),(0,255,0),5)
            font = cv2.FONT_HERSHEY_SIMPLEX
            centerx , centery = change_pt([centerx,centery])
            text = str(centerx) + ','  + str(centery) + ',' + str(theta)
            cv2.putText(frame,text,(10,50), font, 1,(255,255,255),2,cv2.LINE_AA)

            #publish the (x,y,theta) to /shiro_state topic
            state_pub.publish([float(time.time()-tic),float(centerx),float(centery),float(theta)])

        frame = aruco.drawDetectedMarkers(frame,corners)
        cv2.imshow('frame',frame)

        cv2.waitKey(1)
    except CvBridgeError as e:
        print(e)

rospy.init_node("image_getter",anonymous=True)
image_sub = rospy.Subscriber('/android_image',Image,img_cb)
state_pub = rospy.Publisher('/shiro_state',state_msg,queue_size=10)
rospy.spin()
