import numpy as np
import cv2
cap = cv2.VideoCapture('../Dataset/traffic1.avi')
fgbg = cv2.createBackgroundSubtractorMOG2()
while(1):
    ret, frame = cap.read()
    fgmask = fgbg.apply(frame)
    ff =cv2.medianBlur(fgmask,7)
    ret, f = cv2.threshold(ff,127,255,cv2.THRESH_BINARY)
    f = cv2.erode(f, None, iterations=1)
    f = cv2.dilate(f, None, iterations=1)
    cv2.imshow('frame',f)
    cv2.imshow('shadow',ff)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break
cap.release()
cv2.destroyAllWindows()
