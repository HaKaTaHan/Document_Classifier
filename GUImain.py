import math
import time
import sys
from PyQt5 import uic
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import os
import Document_Classifying
import RESULT
from stepListener import interfaceStepListener as stepListener


# Index 0: start
# Index 1: progress
# Index 2: showCover
# Index 3: noCover
# Index 4: choice
# Index 5: finish

timer = time.time()


class InitWindow(QDialog, stepListener):
    def __init__(self):
        QDialog.__init__(self, None)
        uic.loadUi('./GUI/newwindow.ui', self)
        self.btnStart.clicked.connect(self.startprg)
        self.btnComplete.clicked.connect(self.complete)
        self.btnCancel.clicked.connect(self.cancel)
        self.btnPrev.clicked.connect(self.prev)
        self.btnNext.clicked.connect(self.next)
        self.lwList.itemClicked.connect(self.fileClicked)
        self.btnNoCover.clicked.connect(self.noCoverList)
        self.btnToContent.clicked.connect(self.toContentList)
        self.btnComplete.stackUnder(self.btnToContent)
        # GoTo ShowCover
        self.progressBar.valueChanged.connect(self.callShowCover)
        self.btnFinish.clicked.connect(qApp.quit)
        self.__i = 0
        self.__DC = Document_Classifying.Classifying()
        self.__End = object
        self.__coverList = []
        self.__leftList = []
        self.__page = 0
        self.__current_page = 1
        self.__show_list = 10
        self.__selected_key = {}
        self.__dict_pagecount = {}
        self.__dict_originList = {}
        self.__dict_errD = {}
        self.__currentPDF = 0
        self.__currentOCR = 0
        self.__entirePDF = 0
        self.__entireOCR = 0
        self.__entireCrop = 0
        self.__currentGradient = 0
        self.__currentCrop = 0
        self.__currentImprovement = 0
        self.lwList.verticalScrollBar().setStyleSheet("QScrollBar:vertical {border: 0px solid #999999; background: "
                                                      "rgba(0, 0, 0, 1); width: 20px; margin: 0px 0px 0px 0px;}"
                                                      "QScrollBar::handle:vertical {"
                                                      "background: qlineargradient(x1:0, y1:0, x2:1, y2:0,"
                                                      "stop: 0 rgb(255, 163, 139), stop: 0.5 rgb(255, 163, 139),"
                                                      "stop:1 rgb(255, 163, 139));"
                                                      "min-height: 0px;"
                                                      "}")
        self.progressBar.setStyleSheet("QProgressBar {border: 0px; color: rgb(255, 255, 255);}"
                                       "QProgressBar::chunk {background-color: rgb(255, 163, 139);}")

    def callShowCover(self):
        if self.__i == 1:
            self.lblProgress.setText("기울기 보정 중")
        elif self.__i == 2:
            self.lblProgress.setText("모델 분류 중")
        if self.progressBar.value() == 3:
            self.stackedWidget.setCurrentIndex(2)
            self.progressBar.setValue(0)
    #         total 6 levels

    def startprg(self):
        # GoTo ProgressBar
        self.stackedWidget.setCurrentIndex(1)
        print("Start Button Clicked")
        self.__DC.setOnstepListener(self)
        self.__DC.setOnPing(self)
        self.progressBar.setValue(self.__i)
        self.__DC.classify()
        self.__coverList = self.__DC.coverList()

        # if not self.__coverList ~~ origin location
        self.__dict_errD = self.__DC.dictErrD()

        for key in self.__coverList:
            del self.__dict_errD[key]

        if not self.__coverList:
            # GoTo NoCover
            self.stackedWidget.setCurrentIndex(3)
            return
        self.__page = math.ceil(len(self.__coverList) / self.__show_list)
        self.showImage()

    def complete(self):
        print("Clicked Complete")
        temp = self.__selected_key.keys()
        for i in temp:
            self.__coverList.append(i)
        self.__dict_pagecount = self.__DC.pagecount()
        self.__dict_originList = self.__DC.originList()
        self.__End = RESULT.MakeFolder(self.__coverList, self.__dict_pagecount, self.__dict_originList)
        self.__End.make_Result()
        self.__End.unKnown()
        self.btnToContent.stackUnder(self.btnComplete)
        self.stackedWidget.setCurrentIndex(4)

    def noCoverList(self):
        print("Clicked NoCover")
        self.stackedWidget.setCurrentIndex(2)
        self.toContentList()

    def noContentList(self):
        print("Clicked NoContent")
        self.complete()
        self.stackedWidget.setCurrentIndex(4)

    def cancel(self):
        print("Clicked Cancel")
        self.lwList.clearSelection()
        self.__selected_key.clear()

    def isItemSelected(self, item):
        if self.__selected_key.get(item.text(), "new") == "new":
            item.setSelected(0)
        else:
            item.setSelected(1)

    def showImage(self):
        self.lwList.clear()
        if self.__page == 1:
            for i in range(0, len(self.__coverList)):
                item = QListWidgetItem(self.__coverList[i])
                item.setIcon(QIcon(self.__DC.IMG_path + self.__coverList[i]))
                self.lwList.addItem(item)
                self.isItemSelected(item)
        else:
            if self.__current_page != self.__page:
                for i in range((self.__current_page-1)*self.__show_list, self.__current_page*self.__show_list):
                    item = QListWidgetItem(self.__coverList[i])
                    item.setIcon(QIcon(self.__DC.IMG_path + self.__coverList[i]))
                    self.lwList.addItem(item)
                    self.isItemSelected(item)
            else:
                for i in range((self.__current_page-1)*self.__show_list, len(self.__coverList)):
                    item = QListWidgetItem(self.__coverList[i])
                    item.setIcon(QIcon(self.__DC.IMG_path + self.__coverList[i]))
                    self.lwList.addItem(item)
                    self.isItemSelected(item)
        text = str(self.__current_page) + "/" + str(self.__page)
        self.lbIndex.setText(text)


    def showImage2(self):
        self.lwList.clear()
        if self.__page == 1:
            for i in range(0, len(self.__leftList)):
                item = QListWidgetItem(self.__leftList[i][0])
                item.setIcon(QIcon(self.__DC.IMG_path + self.__leftList[i][0]))
                self.lwList.addItem(item)
                self.isItemSelected(item)
        else:
            for i in range(0, 10):
                item = QListWidgetItem(self.__leftList[i][0])
                item.setIcon(QIcon(self.__DC.IMG_path + self.__leftList[i][0]))
                self.lwList.addItem(item)
                self.isItemSelected(item)
        text = "1/1"
        self.lbIndex.setText(text)

    def fileClicked(self, item):
        key = item.text()
        if self.__selected_key.get(key, "new") == "new":
            self.__selected_key[key] = key
        else:
            del self.__selected_key[key]

    def prev(self):
        print("Clicked Prev")
        self.__current_page -= 1
        if self.__current_page < 1:
            self.__current_page = 1
        else:
            self.showImage()

    def next(self):
        print("Clicked Next")
        self.__current_page += 1
        if self.__current_page > self.__page:
            self.__current_page = self.__page
        else:
            self.showImage()


    def upStep(self):
        # progress바 조작하는 곳
        self.__i += self.__DC.Step
        self.progressBar.setValue(self.__i)
        QApplication.processEvents()

    def ping(self):
        self.__currentPDF = self.__currentPDF + 1
        self.lblProgress.setText('PDF -> IMG 변환 중: 전체 ' + str(self.__entirePDF) + '장 중 ' + str(self.__currentPDF) + '장 변환')
        QApplication.processEvents()

    def ocrping(self):
        self.__currentOCR = self.__currentOCR + 1
        self.lblProgress.setText('OCR 검증 중: 전체 ' + str(self.__entireOCR) + '장 중 ' + str(self.__currentOCR) + '장 검증')
        QApplication.processEvents()

    def gradientping(self):
        self.__currentGradient = self.__currentGradient + 1
        self.lblProgress.setText('기울기 보정 중: 전체 ' + str(self.__entirePDF) + '장 중 ' + str(self.__currentGradient) + '장 보정')
        QApplication.processEvents()

    def cropping(self):
        self.__currentCrop = self.__currentCrop + 1
        self.lblProgress.setText('OCR 검증 부분 확인 중: 전체 ' + str(self.__entireCrop) + '장 중 ' + str(self.__currentCrop) + '장 확인')
        QApplication.processEvents()

    def improvementping(self):
        self.__currentImprovement = self.__currentImprovement + 1
        self.lblProgress.setText('이미지 보정 중: 전체 ' + str(self.__entireCrop) + '장 중 ' + str(self.__currentImprovement) + '장 보정')
        QApplication.processEvents()

    def entirePDF(self, num):
        self.__currentPDF = 0
        self.__entirePDF = num
        self.lblProgress.setText('PDF -> IMG 변환 중: 전체 ' + str(self.__entirePDF) + '장 중 ' + str(self.__currentPDF) + '장 변환')
        QApplication.processEvents()

    def entireOCR(self, num):
        print("entireOCR")
        self.__currentOCR = 0
        self.__entireOCR = num
        self.lblProgress.setText('OCR 검증 중: 전체 ' + str(self.__entireOCR) + '장 중 ' + str(self.__currentOCR) + '장 검증')
        QApplication.processEvents()

    def entireCrop(self, num):
        print("entireCrop")
        self.__entireCrop = 0
        self.__entireCrop = num
        self.lblProgress.setText('OCR 검증 부분 확인 중: 전체 ' + str(self.__entireCrop) + '장 중 ' + str(self.__currentCrop) + '장 확인')
        QApplication.processEvents()


    def toContentList(self):
        temp = self.__selected_key.keys()
        for i in temp:
            self.__coverList.remove(i)
        self.__selected_key.clear()
        self.btnPrev.clicked.disconnect(self.prev)
        self.btnNext.clicked.disconnect(self.next)
        self.btnToContent.stackUnder(self.btnComplete)
        self.btnPrev.resize(0, 0)
        self.btnNext.resize(0, 0)
        self.lbIndex.resize(0, 0)

        print(self.__dict_errD)
        # left_List 0 예외처리, noCoverList가 아닌 분류된 Cover - Content들로 생성
        if not self.__dict_errD:
            # GoTo NoCover
            self.btnNoCover.clicked.disconnect(self.noCoverList)
            self.btnNoCover.clicked.connect(self.noContentList)
            self.label.setText("내용으로 분류된 데이터가 없습니다.")
            self.stackedWidget.setCurrentIndex(3)
            return

        # sorted 반환 값 tuple
        self.__leftList = sorted(self.__dict_errD.items(), key=lambda item: item[1])
        print(self.__leftList)
        self.__current_page = 1
        self.__page = math.ceil(len(self.__leftList) / self.__show_list)

        self.showImage2()
        # GoTo ShowContent -> NEED Change to contentProgress





if __name__ == '__main__':
    app = QApplication(sys.argv)
    toShow = InitWindow()
    toShow.show()
    app.exec()