#-*- coding:utf-8 -*-
from PIL import Image
import pytesseract

import os
import image_processing3
from stepListener import interfaceStepListener as stepListener
import time

pytesseract.pytesseract.tesseract_cmd = r'Utils\Tesseract-OCR\tesseract'


class CoverCheck(object):
    def __init__(self, img_path, crop_path, improvement_path, input_string):
        self.__IMG_path = img_path
        self.__CROP_path = crop_path
        self.__Improvement_path = improvement_path
        self.__detail_list = []
        self.__input_detail = input_string.split(',')
        for i in self.__input_detail :
            self.__detail_list.append(i.strip())
        self.__detail_list.sort(key=len, reverse=True)
        self.__Perfect_Cover = {}
        self.__stepListener = stepListener
        self.__IP = image_processing3.IMG_processing(self.__IMG_path, self.__CROP_path, self.__Improvement_path)
        self.__step = 1

    @property
    def Step(self):
        return self.__step

    def crop_from_jpg(self, img):
        temp = Image.open(self.__IMG_path + img)
        width, height = temp.size
        crop_width, crop_height = width, height // 4
        area = (0, 0, crop_width, crop_height)
        crop_img = temp.crop(area)
        crop_img.save(self.__CROP_path + img)

    def crop(self, lists):
        self.__stepListener.entireCrop(len(lists))
        for i in lists:
            self.crop_from_jpg(i)
            self.__stepListener.cropping()
        self.__stepListener.upStepOCR()
        crop_list = os.listdir(self.__CROP_path)
        return crop_list

    def improve(self, lists):
        self.__stepListener.entireCrop(len(lists))
        self.__IP.improve(lists)
        self.__stepListener.upStepOCR()
        improvement_list = os.listdir(self.__Improvement_path)
        return improvement_list

    def log(self, error_file):
        file = open('log.txt', "at")

        file.write(error_file)

        file.close()

    def comparison_with_improvement(self, crop):
        temp = pytesseract.image_to_string(Image.open(self.__Improvement_path+crop), lang='kor')

        self.log('\n' + crop + '\n' + temp + '\n')

        for i in self.__detail_list:
            if temp.find(i) == -1:
                continue
            else:
                temp_list = []

                if self.__Perfect_Cover.get(i) is None:
                    temp_list.append(crop)
                    self.__Perfect_Cover[i] = temp_list
                else:
                    temp_list = self.__Perfect_Cover.get(i)
                    temp_list.append(crop)
                    self.__Perfect_Cover[i] = temp_list
                break


    def comparison(self, lists):

        self.__Perfect_Cover.clear()
        timer = time.time()
        self.__stepListener.entireOCR(len(lists))

        for i in lists:
            self.comparison_with_improvement(i)
            self.__stepListener.ocrping()

        self.__stepListener.upStepOCR()
        print(time.time() - timer)
        return self.__Perfect_Cover

    def setOnstepListener(self, Listner):
        self.__stepListener = Listner
        self.__IP.setOnstepListener(Listner)


if __name__ == "__main__":
    pass


