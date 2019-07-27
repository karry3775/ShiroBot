#!/usr/bin/env python

import rospy
import cv2
import imutils
import numpy as np

cap = cv2.VideoCapture(0)
if cap.isOpened():
    ret,frame = cap.read()

while ret:
    ret,frame = cap.read()
    hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)

    #low and high values for black
    # low = np.array([81,64,28])
    # high = np.array([102,84,48])
    low = np.array([0,0,0])
    high = np.array([40,40,40q])

    image_mask = cv2.inRange(frame,low,high)
    # output = cv2.bitwise_and(frame,frame,mask=image_mask)

    cv2.imshow("original",frame)
    # cv2.imshow("output",output)
    cv2.imshow("image_mask",image_mask)

    #now define ranges of black
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
