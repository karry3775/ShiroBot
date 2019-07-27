#!/usr/bin/env python
import rospy
import numpy as np
import cv2
from cv2 import aruco

"""
drawMarker(...)
drawMarker(dictionary,id,sidePixels[,img[,borderBits]]) -> img
"""
rospy.init_node("aruco_marker_node",anonymous=True)
aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
print(aruco_dict)

#seocnd parameter is id
#last parameter is total image size
img = aruco.drawMarker(aruco_dict,2,500)
cv2.imwrite("aruco_id_2_sm.jpg",img)

cv2.imshow("frame",img)
cv2.waitKey(0)
cv2.destroyAllWindows()
