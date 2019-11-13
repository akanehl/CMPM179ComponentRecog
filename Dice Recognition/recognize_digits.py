import cv2
import numpy as np
#######   training part    ###############
samples = np.loadtxt('generalsamples.data',np.float32)
responses = np.loadtxt('generalresponses.data',np.float32)
responses = responses.reshape((responses.size,1))

model = cv2.ml.KNearest_create()
model.train(samples,cv2.ml.ROW_SAMPLE,responses)

############################# testing part  #########################

cap = cv2.VideoCapture(0)   # '0' is the webcam's ID. usually it is 0 or 1. 'cap' is the video object.
cap.set(15, -4)

counter = 0                             # script will use a counter to handle FPS.
readings = [0, 0]                       # lists are used to track the number of pips.
display = [0, 0]

while True:
    if counter >= 90000:                # set maximum sizes for variables and lists to save memory.
        counter = 0
        readings = [0, 0]
        display = [0, 0]
    ret, im = cap.read()                                    # 'im' will be a frame from the video.
##im = cv2.imread('test.png')
#im = cv2.resize(im,(500,700))

    if counter % 5000 == 0:

        out = np.zeros(im.shape,np.uint8)
        gray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
        thresh = cv2.adaptiveThreshold(gray,255,1,1,11,2)


        contours,hierarchy = cv2.findContours(thresh,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)

        for cnt in contours:
            if cv2.contourArea(cnt)>5000:
                [x,y,w,h] = cv2.boundingRect(cnt)
                if  h>28:
                    cv2.rectangle(im,(x,y),(x+w,y+h),(0,255,0),2)
                    roi = thresh[y:y+h,x:x+w]
                    roismall = cv2.resize(roi,(10,10))
                    roismall = roismall.reshape((1,100))
                    roismall = np.float32(roismall)
                    retval, results, neigh_resp, dists = model.findNearest(roismall, k = 1)
                    string = str(int((results[0][0])))
                    cv2.putText(out,string,(x,y+h),0,1,(0,255,0))

        cv2.imshow('im',im)
        cv2.imshow('out',out)
        key = cv2.waitKey(0)
        if key == 27:  # (escape to quit)
            sys.exit()
