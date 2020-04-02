import os
import shutil
import errno


class MakeFolder(object):
    def __init__(self, coverlist, filepage, originlist):
        self.__Result_path = './Result/'
        self.__IMG_path = './IMG/IMG/'
        self.__coverList = coverlist
        self.__filePage = filepage
        self.__originList = originlist
        self.__eachCover_dict = {}

    def make_Result(self):
        self.make_outFolder()

        self.moveFile()

    def make_outFolder(self):
        for folder in self.__coverList:
            file_numbering, number = folder.split('-')
            originName = self.__originList[file_numbering]

            folderName = originName + " - " + number[:-4]

            try:
                if not (os.path.exists(self.__Result_path + folderName)):
                    os.makedirs(self.__Result_path + folderName)

                self.make_inFolder(folderName, originName, number)
                self.coverDict(file_numbering, number[:-4])

            except OSError as e:
                if e.errno != errno.EEXIST:
                    print("Failed to create directory!!!!!")
                    raise

    def make_inFolder(self, folderName, originName, number):
        cover_folderName = "Cover " + originName + " - " + number[:-4]
        content_folderName = "Content " + originName + " - " + number[:-4]

        try:
            if not (os.path.exists(self.__Result_path + folderName + "/" +cover_folderName)):
                os.makedirs(self.__Result_path + folderName + "/" +cover_folderName)

            if not (os.path.exists(self.__Result_path + folderName + "/" +content_folderName)):
                os.makedirs(self.__Result_path + folderName + "/" +content_folderName)

        except OSError as e:
            if e.errno != errno.EEXIST:
                print("Failed to create directory!!!!!")

    def coverDict(self, fileNumbering, number):
        if self.__eachCover_dict.get(fileNumbering, "new") == "new":
            temp = [int(number)]
            self.__eachCover_dict[fileNumbering] = temp
        else:
            temp = self.__eachCover_dict.get(fileNumbering)
            temp.append(int(number))
            self.__eachCover_dict[fileNumbering] = temp

    def moveFile(self):

        for key in self.__eachCover_dict.keys():
            self.__eachCover_dict[key].sort()
            originName = self.__originList[key]

            for number in range(len(self.__eachCover_dict[key])):
                outFolderpath = self.__Result_path + originName + " - " + str(self.__eachCover_dict[key][number])
                cover_folderName = "Cover " + originName + " - " + str(self.__eachCover_dict[key][number])
                content_folderName = "Content " + originName + " - " + str(self.__eachCover_dict[key][number])

                if number == len(self.__eachCover_dict[key]) - 1:
                    shutil.move(self.__IMG_path + key + "-" + str(self.__eachCover_dict[key][-1]) + ".jpg",
                                outFolderpath + "/" + cover_folderName)
                    for j in range(self.__eachCover_dict[key][-1] + 1, self.__filePage[key] + 1):
                        shutil.move(self.__IMG_path + key + "-" + str(j) + ".jpg",
                                    outFolderpath + "/" + content_folderName)
                    break

                shutil.move(self.__IMG_path + key + "-" + str(self.__eachCover_dict[key][number]) + ".jpg", outFolderpath + "/" + cover_folderName)

                for i in range(self.__eachCover_dict[key][number] + 1, self.__eachCover_dict[key][number + 1]):
                    shutil.move(self.__IMG_path + key + "-" + str(i) + ".jpg", outFolderpath + "/" + content_folderName)

    def unKnown(self):
        folderName = "Unknown"
        if not (os.path.exists(self.__Result_path + folderName)):
            os.makedirs(self.__Result_path + folderName)

        imglist = os.listdir(self.__IMG_path)

        for i in imglist:
            shutil.move(self.__IMG_path + i, self.__Result_path + folderName)


