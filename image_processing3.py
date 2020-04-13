#-*- coding:utf-8 -*-
import cv2
from stepListener import interfaceStepListener as stepListner

class IMG_processing(object):
    def __init__(self, img_path, crop_path, improvement_path):
        self.__IMG_path = img_path
        self.__Crop_path = crop_path
        self.__Improvement_path = improvement_path
        self.__stepListener = stepListner

    def image_processing(self, img):
        temp = cv2.imread(self.__Crop_path+img)

        gray = cv2.cvtColor(temp, cv2.COLOR_BGR2GRAY)

        height, width = gray.shape

        result = cv2.resize(gray, (2 * width, 2 * height), interpolation=cv2.INTER_CUBIC)

        cv2.imwrite(self.__Improvement_path+img, result)

    def improve(self, lists):
        for i in lists:
            self.image_processing(i)
            self.__stepListener.improvementping()
        self.__stepListener.upStepOCR()

    def setOnstepListener(self, Listner):
        self.__stepListener = Listner


if __name__ == "__main__":
    pass
