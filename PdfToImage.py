#-*- coding:utf-8 -*-
from pdf2image import convert_from_path
from PyPDF2 import PdfFileReader
from pdf2image.exceptions import (PDFInfoNotInstalledError, PDFPageCountError, PDFSyntaxError)
import traceback
import shutil
from stepListener import interfaceStepListener as stepListner


class PDFtoIMG(object):
    def __init__(self, pdf_path, img_path):
        self.__PDF_path = pdf_path
        self.__IMG_path = img_path
        self.__RePDF_path = './RePDF/'
        self.__Poppler_path = './Utils/Poppler/bin/'
        self.__pageDict = {}
        self.__originName = {}
        self.__stepListener = stepListner

    def convert_to_img(self, pdf):
        try:
            with open(self.__RePDF_path + pdf, "rb") as f:
                inputpdf = PdfFileReader(f)
                maxPages = inputpdf.numPages
            f.close()

            self.__stepListener.entirePDF(maxPages)
            self.__pageDict[pdf[:-4]] = maxPages

            if maxPages < 5:
                IMG = convert_from_path(self.__RePDF_path + pdf, poppler_path=self.__Poppler_path)
                for j in range(len(IMG)):
                    file = self.__IMG_path + str(pdf[:-4]) + "-" + str(j) + ".jpg"
                    IMG[j].save(file, 'JPEG')
            else:
                for page in range(1, maxPages + 1, 1):
                    IMG = convert_from_path(self.__RePDF_path + pdf, poppler_path=self.__Poppler_path, first_page=page,
                                            last_page=min(page + 1 - 1, maxPages))
                    for j in range(len(IMG)):
                        print(str(page + j) + "/" + str(maxPages))
                        file = self.__IMG_path + str(pdf[:-4]) + "-" + str(page + j) + ".jpg"
                        IMG[j].save(file, 'JPEG')
                        self.__stepListener.ping()

        except PDFPageCountError as countError:
            traceback.print_exc()
        except PDFSyntaxError as syntaxError:
            traceback.print_exc()
        except PDFInfoNotInstalledError as installError:
            traceback.print_exc()
        except Exception as ex:
            print("Error : ", ex)


    def convert(self, lists):
        for i in lists:
            self.convert_to_img(i)

    def rename(self, lists):
        count = 0
        for i in lists:
            shutil.copy(self.__PDF_path+i, self.__RePDF_path+str(count)+".pdf")
            self.__originName[str(count)] = i[:-4]
            count += 1

    def setOnPing(self, Listner):
        self.__stepListener = Listner


    @property
    def RePDF_path(self):
        return self.__RePDF_path

    @property
    def pagecount(self):
        return self.__pageDict

    @property
    def originList(self):
        return self.__originName


if __name__ == "__main__":
    pass

