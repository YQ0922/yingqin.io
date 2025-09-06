# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


import cv2
import numpy as np

def empty(v):
    pass


cap = cv2.VideoCapture(0)

cv2.namedWindow('hsvbar')
cv2.resizeWindow('hsvbar',640,320)
cv2.createTrackbar('Hue Min', 'hsvbar',0, 179,empty)
cv2.createTrackbar('Hue Max', 'hsvbar',179, 179,empty)
cv2.createTrackbar('Sat Min', 'hsvbar',0, 255,empty)
cv2.createTrackbar('Sat Max', 'hsvbar',255, 255,empty)
cv2.createTrackbar('Val Min', 'hsvbar',0, 255,empty)
cv2.createTrackbar('Val Max', 'hsvbar',255, 255,empty)
# hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)

while True:
    h_min = cv2.getTrackbarPos('Hue Min', 'hsvbar')
    h_max = cv2.getTrackbarPos('Hue Max', 'hsvbar')
    s_min = cv2.getTrackbarPos('Sat Min', 'hsvbar')
    s_max = cv2.getTrackbarPos('Sat Max', 'hsvbar')
    v_min = cv2.getTrackbarPos('Val Min', 'hsvbar')
    v_max = cv2.getTrackbarPos('Val Max', 'hsvbar')
    print(h_min,h_max,s_min,s_max,v_min,v_max)

    ret,img = cap.read()
    hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    lower = np.array([h_min, s_min, v_min])
    upper = np.array([h_max,s_max,v_max])

    mask = cv2.inRange(hsv, lower, upper)
    result = cv2.bitwise_and(img,img, mask=mask)

    cv2.imshow('img', img)
    cv2.imshow('mask', mask)
    cv2.imshow('result', result)
    cv2.waitKey(1)



cv2.waitKey(0)

