#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May  9 15:50:48 2024

@author: javed
"""

import cv2
import cv2.aruco as aruco
from servo import dropLoad
VideoCap = False
cap = cv2.VideoCapture(0)
drop=0
im_count=0
def findAruco(img,drop, marker_size=6, total_markers=250, draw=True):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #key = getattr(aruco, f'DICT_{marker_size}X{marker_size}_{total_markers}')
    arucoDict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_4X4_1000)
    #arucoDict = cv2.aruco.Dictionary_get(key)
    arucoParam = aruco.DetectorParameters_create()
    bbox, ids, _ = aruco.detectMarkers(gray, arucoDict, parameters=arucoParam)
    
    if ids is not None:
        for id in ids:
           print(id[0])  # Print each ID
           if id[0] == 69 and drop==0:
                dropLoad()
                print("Payload Drop Sucessful!")
                drop=1
           break

    else:
        print("No markers detected")
        
    if draw:
    	aruco.drawDetectedMarkers(img,bbox,ids)
    return bbox,ids,drop

while True:
    _,img=cap.read()
    if img is None:
        print("Error: Failed to capture frame from the camera.")
        break

    bbox,ids,drop=findAruco(img,drop)
    if cv2.waitKey(1)==113:
        break
    #cv2.imshow("img",img)
    name=str(im_count)+'data.jpg'
    cv2.imwrite(name,img)
    im_count +=1
    cv2.imwrite("/var/www/html/frameVid.jpg", img)
    
    
