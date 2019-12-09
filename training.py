import sys

import numpy as np
import cv2

def rotateImage(image, angle):

  image_center = tuple(np.array(image.shape[1::-1]) / 2)
  rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
  result = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR)
  return result
def main():
    samples =  np.empty((0,100))
    responses = []
    keys = [i for i in range(48,58)]

    cap = cv2.VideoCapture(0)   # '0' is the webcam's ID. usually it is 0 or 1. 'cap' is the video object.
    cap.set(15, -5)
    isTraining = True;

    while isTraining:
        cv2.destroyWindow('Quit')

        ret, im = cap.read()  # 'im' will be a frame from the video.
        im3 = im.copy()

        prevX = -1

        currentRotation = 0 # Set inital rotation

        cv2.imshow('Norm',im)

        while(currentRotation < 360):
            gray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
            blur = cv2.GaussianBlur(gray,(5,5),0)
            thresh = cv2.adaptiveThreshold(blur,255,1,1,11,2)
            cv2.imshow('thresh',thresh)

        #################      Now finding Contours         ###################
            contours,hierarchy = cv2.findContours(thresh,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
            for cnt in contours:
                area = cv2.contourArea(cnt)
                if (area > 700 and area <= 900):
                    [x,y,w,h] = cv2.boundingRect(cnt)

                    if  h>28:
                        cv2.rectangle(im,(x,y),(x+w,y+h),(0,0,255),2)
                        roi = thresh[y:y+h,x:x+w]
                        roismall = cv2.resize(roi,(10,10))
                        cv2.imshow('Norm',im)


                        key = cv2.waitKey(0)
                        if key == 27:  # (escape to quit)
                            break
                        elif key in keys:
                            print(area)

                            prevX = cv2.contourArea(cnt)

                            responses.append(int(chr(key)))
                            sample = roismall.reshape((1,100))
                            samples = np.append(samples,sample,0)
        #################      Now Increaseing Rotation         ###################
            currentRotation += 10
            im = rotateImage(im3, currentRotation)

        cv2.imshow('Quit',im)
        key = cv2.waitKey(0) # wait for next role
        if key == 27:  # (escape to quit)
            isTraining = False;
        cv2.destroyWindow('Quit?')

    responses = np.array(responses,np.float32)
    responses = responses.reshape((responses.size,1))

    print ("training complete")

    np.savetxt('generalsamples.data',samples)
    np.savetxt('generalresponses.data',responses)

main()
