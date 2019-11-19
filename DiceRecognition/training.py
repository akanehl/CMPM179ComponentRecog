import sys

import numpy as np
import cv2


samples =  np.empty((0,100))
responses = []
keys = [i for i in range(48,58)]

cap = cv2.VideoCapture(0)   # '0' is the webcam's ID. usually it is 0 or 1. 'cap' is the video object.
cap.set(15, -4)

isTraing = True;
while isTraing:
    ret, im = cap.read()  # 'im' will be a frame from the video.
    im3 = im.copy()

    cv2.imshow('norm',im)
    key = cv2.waitKey(0) # wait for next role
    if key == 27:  # (escape to quit)
        break
        sys.exit()



    gray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray,(5,5),0)
    thresh = cv2.adaptiveThreshold(blur,255,1,1,11,2)
    cv2.imshow('thresh',thresh)
#################      Now finding Contours         ###################

    contours,hierarchy = cv2.findContours(thresh,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)

    for cnt in contours:
        if cv2.contourArea(cnt)>500:
            [x,y,w,h] = cv2.boundingRect(cnt)

            if  h>28:
                cv2.rectangle(im,(x,y),(x+w,y+h),(0,0,255),2)
                roi = thresh[y:y+h,x:x+w]
                roismall = cv2.resize(roi,(10,10))
                cv2.imshow('norm',im)

                key = cv2.waitKey(0)

                if key == 27:  # (escape to quit)
                    break
                    sys.exit()
                elif key in keys:
                    responses.append(int(chr(key)))
                    sample = roismall.reshape((1,100))
                    samples = np.append(samples,sample,0)

responses = np.array(responses,np.float32)
responses = responses.reshape((responses.size,1))
print ("training complete")

np.savetxt('generalsamples.data',samples)
np.savetxt('generalresponses.data',responses)
