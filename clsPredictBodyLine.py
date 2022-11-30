#####################################################
#### Written By: SATYAKI DE                      ####
#### Written On: 20-Nov-2022                     ####
#### Modified On 30-Nov-2022                     ####
####                                             ####
#### Objective: This is the main calling         ####
#### python script that will invoke the          ####
#### clsPredictBodyLine class to initiate        ####
#### the prediction capability in real-time      ####
#### & display the result from a live sports.    ####
#####################################################

import cv2
import cvzone
from cvzone.ColorModule import ColorFinder
from clsKalmanFilter import clsKalmanFilter

from clsConfigClient import clsConfigClient as cf
import numpy as np
import math

import ssl
import time

# Bypassing SSL Authentication
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    # Legacy python that doesn't verify HTTPS certificates by default
    pass
else:
    # Handle target environment that doesn't support HTTPS verification
    ssl._create_default_https_context = _create_unverified_https_context

# Disbling Warning
def warn(*args, **kwargs):
    pass

import warnings
warnings.warn = warn

###############################################
###           Global Section                ###
###############################################

# Load Kalman filter to predict the trajectory
kf = clsKalmanFilter()

# Create the color ColorFinder
myColorFinder = ColorFinder(False)

posListX = []
posListY = []

xList = [item for item in range(0, 1300)]
prediction=False

###############################################
###    End of Global Section                ###
###############################################

class clsPredictBodyLine(object):
    def __init__(self):
        self.inputFile_1 = str(cf.conf['BASE_FILE'])
        self.inputFile_2 = str(cf.conf['BASE_IMAGE_FILE'])
        self.src_path = str(cf.conf['SRC_PATH'])
        self.hsvVals = cf.conf['HSV']
        self.pauseTime = cf.conf['PAUSE']
        self.pT1 = int(cf.conf['POINT_1'])
        self.pT2 = int(cf.conf['POINT_2'])
        self.pT3 = int(cf.conf['POINT_3'])
        self.pT4 = int(cf.conf['POINT_4'])

    def predStream(self, img, hsvVals, FrNo):
        try:
            pT1 = self.pT1
            pT2 = self.pT2
            pT3 = self.pT3
            pT4 = self.pT4

            #Find the color ball
            imgColor, mask = myColorFinder.update(img, hsvVals)

            #Find location of the red_ball
            imgContours, contours = cvzone.findContours(img, mask, minArea=500)

            if contours:
                posListX.append(contours[0]['center'][0])
                posListY.append(contours[0]['center'][1])

            if posListX:
                # Find the Coefficients
                A, B, C = np.polyfit(posListX, posListY, 2)

                for i, (posX, posY) in enumerate(zip(posListX, posListY)):
                    pos = (posX, posY)
                    cv2.circle(imgContours, pos, 10, (0,255,0), cv2.FILLED)

                    # Using Karman Filter Prediction
                    predicted = kf.predict(posX, posY)
                    cv2.circle(imgContours, (predicted[0], predicted[1]), 12, (255,0,255), cv2.FILLED)

                    ballDetectFlag = True
                    if ballDetectFlag:
                        print('Balls Detected!')

                    if i == 0:
                        cv2.line(imgContours, pos, pos, (0,255,0), 5)
                        cv2.line(imgContours, predicted, predicted, (255,0,255), 5)
                    else:
                        predictedM = kf.predict(posListX[i-1], posListY[i-1])

                        cv2.line(imgContours, pos, (posListX[i-1], posListY[i-1]), (0,255,0), 5)
                        cv2.line(imgContours, predicted, predictedM, (255,0,255), 5)

                if len(posListX) < 10:

                    # Calculation for best place to ball
                    a1 = A
                    b1 = B
                    c1 = C - pT1

                    X1 = int((- b1 - math.sqrt(b1**2 - (4*a1*c1)))/(2*a1))
                    prediction1 = pT2 < X1 < pT3

                    a2 = A
                    b2 = B
                    c2 = C - pT4

                    X2 = int((- b2 - math.sqrt(b2**2 - (4*a2*c2)))/(2*a2))
                    prediction2 = pT2 < X2 < pT3

                    prediction = prediction1 | prediction2

                if prediction:
                    print('Good Length Ball!')
                    sMsg = "Good Length Ball - (" + str(FrNo) + ")"
                    cvzone.putTextRect(imgContours, sMsg, (50,150), scale=5, thickness=5, colorR=(0,200,0), offset=20)
                else:
                    print('Loose Ball!')
                    sMsg = "Loose Ball - (" + str(FrNo) + ")"
                    cvzone.putTextRect(imgContours, sMsg, (50,150), scale=5, thickness=5, colorR=(0,0,200), offset=20)

                return imgContours

        except Exception as e:
            x = str(e)
            print('Error predStream:', x)

            return img

    def processVideo(self, debugInd, var):
        try:
            cnt = 0
            lastRowFlag=True
            breakFlag = False
            pauseTime = self.pauseTime
            src_path = self.src_path
            inputFile_1 = self.inputFile_1
            inputFile_2 = self.inputFile_2
            hsvVals = self.hsvVals

            FileName_1 = src_path + inputFile_1
            FileName_2 = src_path + inputFile_2

            # Initialize the video
            cap = cv2.VideoCapture(FileName_1)

            while True:
                try:
                    if breakFlag:
                        break

                    # Grab the frames
                    success, img = cap.read()
                    time.sleep(pauseTime)

                    cnt+=1

                    print('*'*60)
                    print('Frame Number:', str(cnt))

                    if (cv2.waitKey(1) & 0xFF) == ord("q"):
                        break

                    if success:

                        imgContours = self.predStream(img, hsvVals, cnt)

                        if imgContours is None:
                            imgContours = img

                        imgColor = cv2.resize(imgContours, (0,0), None, 0.7, 0.7)

                        # Display
                        cv2.imshow("ImageColor", imgColor)

                        print('*'*60)
                    else:
                        #breakFlag=True
                        pass

                except Exception as e:
                    x = str(e)
                    print('Error Main:', x)

            cv2.destroyAllWindows()

            return 0

        except Exception as e:
            x = str(e)
            print('Error:', x)

            cv2.destroyAllWindows()

            return 1
