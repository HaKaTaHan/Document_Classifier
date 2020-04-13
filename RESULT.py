import os
import shutil
import errno

#self.__coverList = 모델이 제목으로 분류한 리스트
#self.__filePage = 딕셔너리 key : 파일 원래 이름 value : 해당 파일 장수
#self.__originList = 딕셔너리 key : repdf number value : 해당 repdf 원래 파일명
#self.__eachCover_dict = cover 파일에 맞는 content를 담은 딕셔너리 key : cover명 value : 해당 cover의 content


class MakeFolder(object):
    def __init__(self, coverlist, filepage, originlist):
        self.__Result_path = './Result/'
        self.__IMG_path = './IMG/IMG/'
        self.__coverList = coverlist
        self.__filePage = filepage
        self.__originList = originlist
        self.__eachCover_dict = {}

    def make_Result(self):
        print("make_Result")
        self.coverDict()
        
        self.make_outFolder()

        IMGlist = os.listdir(self.__IMG_path)

        if len(IMGlist) != 0:
            self.unKnown()

    def coverDict(self):
        print("coverDict")

        for cover in range(len(self.__coverList)):
            contentList = []

            pdfnum, filenum = map(int, self.__coverList[cover][:-4].split('-'))
            originPdfCount = self.__filePage.get(str(pdfnum))

            for content in range(filenum + 1, originPdfCount + 1):
                contentFile = str(pdfnum) + "-" + str(content) + ".jpg"

                if contentFile in self.__coverList:
                    break

                contentList.append(contentFile)

            self.__eachCover_dict[self.__coverList[cover]] = contentList

    def make_outFolder(self):
        print("make_outFolder")

        for folder in list(self.__eachCover_dict.keys()):
            file_numbering, number = folder[:-4].split('-')
            originName = self.__originList[file_numbering]
            FolderName = originName + " - " + number

            try:
                if not (os.path.exists(self.__Result_path + FolderName)):
                    os.makedirs(self.__Result_path + FolderName)

                self.make_inFolder(FolderName, originName, number, folder)
            except OSError as e:
                if e.errno != errno.EEXIST:
                    print("Failed to create outFolder directory!!!!!")
                    raise
            except Exception as ex:
                print("Error : ", ex)
                raise

    def make_inFolder(self, folderName, originName, number, cover):
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

    def moveFile(self, folderName, coverFolder, contentFolder, cover):
        print("moveFile")
        contents = self.__eachCover_dict.get(cover)

        shutil.move(self.__IMG_path + cover, self.__Result_path + folderName + "/" + coverFolder)

        for content in contents:
            shutil.move(self.__IMG_path + content, self.__Result_path + folderName + "/" + contentFolder)

    def unKnown(self):
        print("unKnown")
        folderName = "Unknown"

        if not (os.path.exists(self.__Result_path + folderName)):
            os.makedirs(self.__Result_path + folderName)

        imglist = os.listdir(self.__IMG_path)

        for i in imglist:
            shutil.move(self.__IMG_path + i, self.__Result_path + folderName)
        