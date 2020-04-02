#-*- coding:utf-8 -*-
from PIL import Image
import pytesseract
from stepListener import interfaceStepListener as stepListener
import cv2
import time

pytesseract.pytesseract.tesseract_cmd = r'Utils\Tesseract-OCR\tesseract'


class CoverCheck(object):
    def __init__(self, img_path, crop_path, improvement_path):
        self.__IMG_path = img_path
        self.__CROP_path = crop_path
        self.__Improvement_path = improvement_path
        self.__case = ['서식', '수신자', '제 목', '귀하', '통지']
        self.__Perfect_Cover = []
        self.__stepListener = stepListener

    def crop_from_jpg(self, img):
        temp = Image.open(self.__IMG_path + img)
        width, height = temp.size
        crop_width, crop_height = width, height // 3
        area = (0, 0, crop_width, crop_height)
        crop_img = temp.crop(area)
        crop_img.save(self.__CROP_path + img)

    def crop(self, lists):
        self.__stepListener.upStep()
        self.__stepListener.entireCrop(len(lists))
        for i in lists:
            self.crop_from_jpg(i)
            self.__stepListener.cropping()

        self.__stepListener.upStep()

    def log(self, error_file):
        file = open('log.txt', "at")

        file.write(error_file)

        file.close()

    def comparison_with_improvement(self, crop):
        temp = pytesseract.image_to_string(Image.open(self.__Improvement_path+crop), lang='kor')

        for i in self.__case:
            if temp.find(i) == -1:
                continue
            else:
                return True

        self.log('\n' + crop + '\n' + temp + '\n')

        return False

    def comparison(self, lists):

        self.__Perfect_Cover.clear()
        timer = time.time()
        self.__stepListener.entireOCR(len(lists))

        for i in lists:
            if self.comparison_with_improvement(i):
                self.__Perfect_Cover.append(i)
            self.__stepListener.ocrping()

        self.__stepListener.upStep()
        print(time.time() - timer)
        return self.__Perfect_Cover

    def setOnstepListener(self, Listner):
        self.__stepListener = Listner


if __name__ == "__main__":
    pass


