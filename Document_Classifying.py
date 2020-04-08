#-*- coding:utf-8 -*-
import os
import PdfToImage
import gradient
from stepListener import interfaceStepListener as stepListner
import GPUmodelLoad1


class Classifying(object):
    def __init__(self):
        self.__IMG_path = './IMG/IMG/'
        self.__PDF_path = './PDF/'
        self.__CROP_path = './CROP/'
        self.__Improvement_path = './Improvement/'
        self.__PTI = PdfToImage.PDFtoIMG(self.__PDF_path, self.__IMG_path)
        self.__Gradient = gradient.mod_gradient(self.__IMG_path)
        self.__coverlist = []
        self.__step = 1
        self.__stepListener = stepListner
        self.__Model1 = None
        self.__dictErrD = {}

    @property
    def PDF_path(self):
        return self.__PDF_path

    @property
    def IMG_path(self):
        return self.__IMG_path

    @property
    def Crop_path(self):
        return self.__CROP_path

    @property
    def Improvement_path(self):
        return self.__Improvement_path

    @property
    def Step(self):
        return self.__step

    def classify(self):
        # PDF -> JPG
        pdf_list = os.listdir(self.__PDF_path)

        self.__PTI.rename(pdf_list)

        rePdf_list = os.listdir(self.__PTI.RePDF_path)

        self.__PTI.convert(rePdf_list)

        imglist = os.listdir(self.__IMG_path)

        # pdf -> img 변환 끝남
        self.__stepListener.upStep()

        self.__Gradient.Gradient(imglist)
        # 기울기 보정 끝남
        self.__stepListener.upStep()

        self.__Model1 = GPUmodelLoad1.model()
        self.__Model1.showGan()

        self.__coverlist = self.__Model1.identify_cover()
        self.__dictErrD = self.__Model1.dictErrD()

        self.__stepListener.upStep()
        # self.CROP_clear()
        # self.IMPROVEMENT_clear()
        self.REPDF_clear()

    def IMG_clear(self):
        temp_imgs = os.listdir(self.__IMG_path)
        print(temp_imgs)

        for i in temp_imgs:
            os.remove(self.__IMG_path+i)

        return True

    def CROP_clear(self):
        temp_imgs = os.listdir(self.__CROP_path)

        for i in temp_imgs:
            os.remove(self.__CROP_path + i)

        return True

    def IMPROVEMENT_clear(self):
        temp_imgs = os.listdir(self.__Improvement_path)

        for i in temp_imgs:
            os.remove(self.__Improvement_path + i)

        return True

    def REPDF_clear(self):
        temp_pdfs = os.listdir(self.__PTI.RePDF_path)

        for i in temp_pdfs:
            os.remove(self.__PTI.RePDF_path + i)

    def coverList(self):
        return self.__coverlist

    def pagecount(self):
        return self.__PTI.pagecount

    def originList(self):
        return self.__PTI.originList

    def dictErrD(self):
        return self.__dictErrD

    def setOnstepListener(self, Listner):
        self.__stepListener = Listner
        self.__Gradient.setOnstepListener(Listner)

    def setOnPing(self, listener):
        self.__PTI.setOnPing(listener)



