#-*- coding:utf-8 -*-
import cv2
import numpy as np
from stepListener import interfaceStepListener as stepListener


class mod_gradient(object):
    def __init__(self, img_path):
        self.__IMG_path = img_path
        self.__stepListener = stepListener

    def pregradient(self, img):
        temp = cv2.imread(self.__IMG_path+img)

        gray = cv2.cvtColor(temp, cv2.COLOR_BGR2GRAY)
        gray = cv2.bitwise_not(gray)

        thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
        coords = np.column_stack(np.where(thresh > 0))
        angle = cv2.minAreaRect(coords)[-1]

        if angle < -45:
            angle = -(90 + angle)
        else:
            angle = -angle

        (h, w) = gray.shape[:2]
        center = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D(center, angle, 1.0)
        rotated = cv2.warpAffine(temp, M, (w, h), borderMode=cv2.BORDER_REPLICATE)
        cv2.imwrite(self.__IMG_path+img, rotated)

    def Gradient(self, lists):
        for i in lists:
            self.pregradient(i)
            self.__stepListener.gradientping()

    def setOnstepListener(self, Listner):
        self.__stepListener = Listner