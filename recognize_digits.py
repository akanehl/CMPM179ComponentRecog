import cv2
import numpy as np
import statistics

#######   training part    ###############
samples = np.loadtxt('generalsamples.data',np.float32)
responses = np.loadtxt('generalresponses.data',np.float32)
responses = responses.reshape((responses.size,1))

model = cv2.ml.KNearest_create()
model.train(samples,cv2.ml.ROW_SAMPLE,responses)

############################# testing part  #########################

cap = cv2.VideoCapture(0)   # '0' is the webcam's ID. usually it is 0 or 1. 'cap' is the video object.
cap.set(15, -5) # '15' references video's brightness. '-4' sets the brightness.

counter = 0                             # script will use a counter to handle FPS.
readings = [-1,-1]                       # lists are used to track the number of pips.
display = [0, 0]
isRunning = True
imgSamples = 64

while isRunning:
    if counter >= 90000:   # set maximum sizes for variables and lists to save memory.
        counter = 0
        readings = [-1,-1]
        display = [0, 0]
    posx = 100
    posy = 100
    posh= 50

    for smpl in range(imgSamples):
        ret, im = cap.read()  # 'im' will be a frame from the video.

        out = np.zeros(im.shape,np.uint8)
        gray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray,(5,5),0)
        thresh = cv2.adaptiveThreshold(blur,255,1,1,11,2)


        contours,hierarchy = cv2.findContours(thresh,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)

        for cnt in contours:
            if (cv2.contourArea(cnt) < 900 and cv2.contourArea(cnt) > 700):
                [x,y,w,h] = cv2.boundingRect(cnt)
                if  h>28:
                    posx = x
                    posy = y
                    posh = h
                    cv2.rectangle(im,(x,y),(x+w,y+h),(0,255,0),2)
                    roi = thresh[y:y+h,x:x+w]
                    roismall = cv2.resize(roi,(10,10))
                    roismall = roismall.reshape((1,100))
                    roismall = np.float32(roismall)
                    retval, results, neigh_resp, dists = model.findNearest(roismall, k = 1)
                    string = str(int((results[0][0]))) #the result parsed to a string to output an image
                    readNum = int(string) #revert the result back into an int to display to console and to have a tangible number to work with
                    readings.append(readNum)

    print(readings)
    number = statistics.mode(readings)
    readings = [-1,-1]
    if(number == -1):
        number ="NO DICE"
    cv2.putText(out,str(number),(posx,posy+posh),0,1,(0,255,0))
    cv2.imshow('out',out)
    cv2.imshow('im',im)
    key = cv2.waitKey(0)
    if key == 27:  # (escape to quit)
        isRunning = False
cap.release()
cv2.destroyAllWindows()
