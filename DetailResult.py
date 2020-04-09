import os
import shutil
import errno

#self.__coverList = 모델이 제목으로 분류한 리스트
#self.__filePage = 딕셔너리 key : 파일 원래 이름 value : 해당 파일 장수
#self.__originList = 딕셔너리 key : repdf number value : 해당 repdf 원래 파일명
#self.__classifyName = 사용자가 입력한 세부 분류명 딕셔너리 key : 분류명 value : 해당 하는 파일명 리스트
#self.__classifyNormalCover = cover 파일에 맞는 content를 담은 딕셔너리 key : cover명 value : 해당 cover의 content
#self.__classifyOCRCover = 사용자가 입력한 분류명에 해당하는 제목 파일만 담은 리스트


class MakeDetailFolder(object):
    def __init__(self, coverlist, filepage, originlist, input_detail):
        self.__Result_path = './Result/'
        self.__IMG_path = './IMG/IMG/'
        self.__coverList = coverlist
        self.__filePage = filepage
        self.__originList = originlist
        self.__classifyName = input_detail
        self.__classifyNormalCover = {}
        self.__classifyOCRCover = []

    def makeResult(self):
        print("makeResult")
        self.makeCoverDict()
        print(self.__classifyNormalCover)
        self.makeOutFolder()

        IMGlist = os.listdir(self.__IMG_path)

        if len(IMGlist) != 0:
            self.unKnown()


    #가장 바깥 폴더
    def makeOutFolder(self):
        print("makeOutFolder")
        #전체 커버리스트 중에서 OCR로 분류한 커버 분리
        for detailCoverKey in list(self.__classifyName.keys()):
            for detailCover in self.__classifyName.get(detailCoverKey):
                self.__coverList.remove(detailCover)
                self.__classifyOCRCover.append(detailCover)

        print("coverlist", self.__coverList)
        print("ocrlist", self.__classifyOCRCover)

        #1. 사용자가 입력한 세부 분류명으로 폴더를 만든다.
        for folder in list(self.__classifyName.keys()):
            try:
                if not (os.path.exists(self.__Result_path + folder)):
                    os.makedirs(self.__Result_path + folder)

                    self.makeOCRFolder(folder)
                        
            except OSError as e:
                if e.errno != errno.EEXIST:
                    print("Failed to create outFolder directory!!!!!")
                    raise

        if len(os.listdir(self.__IMG_path)) != 0:
            #2. 기타 폴더 생성(기존 RESULT 방식 저장)
            folderName = "기타"

            try:
                if not (os.path.exists(self.__Result_path + folderName)):
                    os.makedirs(self.__Result_path + folderName)

                    self.makeetcFolder(folderName)

            except OSError as e:
                if e.errno != errno.EEXIST:
                    print("Failed to create directory!!!!!")
                    raise
            except Exception as ex:
                print("Error : ", ex)
                raise

    #사용자 분류명 내부 폴더 생성
    def makeOCRFolder(self, folderName):
        print("makeOCRFolder")
        FileNameList = self.__classifyName.get(folderName)

        for detailFolder in FileNameList:
            file_numbering, number = detailFolder[:-4].split('-')
            originName = self.__originList[file_numbering]
            OCRFolderName = folderName + "/" + originName + " - " + number

            try:
                if not (os.path.exists(self.__Result_path + OCRFolderName)):
                    os.makedirs(self.__Result_path + OCRFolderName)

                    self.makeInFolder(OCRFolderName, originName, number, detailFolder)

            except OSError as e:
                if e.errno != errno.EEXIST:
                    print("Failed to create OCRFolder directory!!!!!")
                    raise
            except Exception as ex:
                print("Error : ", ex)
                raise

    #기타 내부 폴더 생성
    def makeetcFolder(self, folderName):
        print("makeetcFolder")
        for etcfolder in self.__coverList:
            file_numbering, number = etcfolder[:-4].split('-')
            originName = self.__originList[file_numbering]
            etcFolderName = folderName + "/" + originName + " - " + number

            try:
                if not (os.path.exists(self.__Result_path + etcFolderName)):
                    os.makedirs(self.__Result_path + etcFolderName)

                    self.makeInFolder(etcFolderName, originName, number, etcfolder)

            except OSError as e:
                if e.errno != errno.EEXIST:
                    print("Failed to create etcFolder directory!!!!!")
                    raise
            except Exception as ex:
                print("Error : ", ex)
                raise

    #세부 폴더 생성
    def makeInFolder(self, folderName, originName, number, cover):
        print("makeInFolder")
        cover_folderName = "Cover " + originName + " - " + number
        content_folderName = "Content " + originName + " - " + number

        try:
            if not (os.path.exists(self.__Result_path + folderName + "/" +cover_folderName)):
                os.makedirs(self.__Result_path + folderName + "/" +cover_folderName)

            if not (os.path.exists(self.__Result_path + folderName + "/" +content_folderName)):
                os.makedirs(self.__Result_path + folderName + "/" +content_folderName)

            self.moveFile(folderName, cover_folderName, content_folderName, cover)

        except OSError as e:
            if e.errno != errno.EEXIST:
                print("Failed to create InFolder directory!!!!!")
                raise
        except Exception as ex:
            print("Error : ", ex)
            raise
        
    #전체 파일을 cover별 묶음 분류(데이터 상으로)
    def makeCoverDict(self):
        print("makeCoverDict")

        for cover in range(len(self.__coverList)):
            contentList = []

            pdfnum, filenum = map(int, self.__coverList[cover][:-4].split('-'))
            originPdfCount = self.__filePage.get(str(pdfnum))

            for content in range(filenum + 1, originPdfCount + 1):
                contentFile = str(pdfnum) + "-" + str(content) + ".jpg"

                if contentFile in self.__coverList:
                    break

                contentList.append(contentFile)

            self.__classifyNormalCover[self.__coverList[cover]] = contentList
            # #마지막 cover파일일 때
            # if cover == len(self.__coverList) - 1:
            #     pdfnum, filenum = map(int, self.__coverList[cover][:-4].split('-'))
            #     originPdfCount = self.__filePage.get(str(pdfnum))
            #
            #     for content in range(filenum + 1, originPdfCount + 1):
            #         contentFile = str(pdfnum) + "-" + str(content) + ".jpg"
            #
            #         # 만약 도중에 제목을 만날 경우
            #         if contentFile in self.__coverList:
            #             break
            #
            #         contentList.append(contentFile)
            #     self.__classifyNormalCover[self.__coverList[cover]] = contentList
            #     break
            #
            # now_pdfnum, now_filenum = map(int, self.__coverList[cover][:-4].split('-'))
            # next_pdfnum, next_filenum = map(int, self.__coverList[cover+1][:-4].split('-'))
            #
            # #now_pdfnum과 next_pdfnum 다를 때 즉 pdf파일이 바뀌었을 때
            # if now_pdfnum != next_pdfnum:
            #     originPdfCount = self.__filePage.get(str(now_pdfnum))
            #
            #     for content in range(now_filenum + 1, originPdfCount + 1):
            #         contentFile = str(now_pdfnum) + "-" + str(content) + ".jpg"
            #
            #         #만약 도중에 제목을 만날 경우
            #         if contentFile in self.__coverList:
            #             break
            #
            #         contentList.append(contentFile)
            #
            #     self.__classifyNormalCover[self.__coverList[cover]] = contentList
            # else:
            #     for content in range(now_filenum + 1, next_filenum):
            #         contentFile = str(now_pdfnum) + "-" + str(content) + ".jpg"
            #
            #         # 만약 도중에 제목을 만날 경우
            #         if contentFile in self.__coverList:
            #             break
            #
            #         contentList.append(contentFile)
            #     self.__classifyNormalCover[self.__coverList[cover]] = contentList

    #이미지 알맞게 옮기기(cover에 오는 파일명을 key로 self.__classifyNormalCover에서 value 찾아서 각각 coverfolder와 contentfolder로 이동 )
    def moveFile(self, folderName, coverFolder, contentFolder, cover):
        print("moveFile")
        contents = self.__classifyNormalCover.get(cover)
        #제목 파일 옮기기
        shutil.move(self.__IMG_path + cover, self.__Result_path + folderName + "/" + coverFolder)
        #내용 파일 옮기기
        for content in contents:
            shutil.move(self.__IMG_path + content, self.__Result_path + folderName + "/" + contentFolder)

    #어디로 가야할 지 모르는 이미지들 처리 폴더
    def unKnown(self):
        print("unKnown")
        folderName = "Unknown"

        if not (os.path.exists(self.__Result_path + folderName)):
            os.makedirs(self.__Result_path + folderName)

        imglist = os.listdir(self.__IMG_path)

        for i in imglist:
            shutil.move(self.__IMG_path + i, self.__Result_path + folderName)

