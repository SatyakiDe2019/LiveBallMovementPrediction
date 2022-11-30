############################################
#### Enhanced By: SATYAKI DE        ########
#### Enhanced On: 30-Nov-2022       ########
############################################

import cv2
import numpy as np

class clsKalmanFilter:
    kf = cv2.KalmanFilter(4, 2)
    kf.measurementMatrix = np.array([[1, 0, 0, 0], [0, 1, 0, 0]], np.float32)
    kf.transitionMatrix = np.array([[1, 0, 1, 0], [0, 1, 0, 1], [0, 0, 1, 0], [0, 0, 0, 1]], np.float32)

    # This function estimates the position of the object
    def predict(self, coordX, coordY):
        try:

            measured = np.array([[np.float32(coordX)], [np.float32(coordY)]])
            self.kf.correct(measured)
            predicted = self.kf.predict()
            x, y = int(predicted[0]), int(predicted[1])
            return x, y

        except Exception as e:
            k = str(e)
            print('Error: ', k)

            x, y = ()
            return x, y
