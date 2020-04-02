#-*- coding:utf-8 -*-
import os
import torch
import torch.nn as nn
import torch.nn.parallel
import torch.utils.data
import torchvision.datasets as dset
import torchvision.transforms as transforms
import numpy as np
import random
from collections import OrderedDict

torch.manual_seed(0)
np.random.seed(0)
torch.backends.cudnn.deterministic = True
torch.backends.cudnn.benchmark = False
torch.backends.cudnn.enabled = False
random.seed(999)
torch.manual_seed(999)

class Generator(nn.Module):
    def __init__(self, ngpu):
        self.__ngf = 32
        self.__ndf = 32
        self.__nc = 3
        super(Generator, self).__init__()
        self.__ngpu = ngpu
        self.__main = nn.Sequential(
            nn.ConvTranspose2d(self.__ngf * 4, self.__ngf * 4, 4, 1, 0, bias=False),
            nn.BatchNorm2d(self.__ngf * 4),
            nn.ReLU(True),
            nn.ConvTranspose2d(self.__ngf * 4, self.__ngf * 2, 4, 2, 1, bias=False),
            nn.BatchNorm2d(self.__ngf * 2),
            nn.ReLU(True),
            nn.ConvTranspose2d(self.__ngf * 2, self.__ngf, 4, 2, 1, bias=False),
            nn.BatchNorm2d(self.__ngf),
            nn.ReLU(True),
            nn.ConvTranspose2d(self.__ngf, self.__nc, 4, 2, 1, bias=False),
            nn.Tanh()
        )

    def forward(self, input):
        return self.__main(input)

class Discriminator(nn.Module):
    def __init__(self, ngpu):
        self.__ngf = 32
        self.__ndf = 32
        self.__nc = 3
        super(Discriminator, self).__init__()
        self.__ngpu = ngpu
        self.__main = nn.Sequential(
            nn.Conv2d(self.__nc, self.__ndf, 4, 2, 1, bias=False),
            nn.LeakyReLU(0.2, inplace=True),
            nn.Conv2d(self.__ndf, self.__ndf * 2, 4, 2, 1, bias=False),
            nn.BatchNorm2d(self.__ndf * 2),
            nn.LeakyReLU(0.2, inplace=True),
            nn.Conv2d(self.__ndf * 2, self.__ndf * 4, 4, 2, 1, bias=False),
            nn.BatchNorm2d(self.__ndf * 4),
            nn.LeakyReLU(0.2, inplace=True),
            nn.Conv2d(self.__ndf * 4, 1, 4, 1, 0, bias=False),
            nn.Sigmoid()
        )

    def forward(self, input):
        return self.__main(input)

class model(object):
    # def __init__(self, ocr, ip, crop_path, improvement_path):
    def __init__(self):
        self.__modelG = Generator(1)
        self.__modelG.cuda()
        self.__modelD = Discriminator(1)
        self.__modelG.cuda()
        self.__dataroot = './IMG'
        self.__img_size = 32
        self.__batch_size = 1
        self.__workers = 2
        self.__train_data_name = os.listdir(self.__dataroot+'/IMG')
        self.__train_data = dset.ImageFolder(root = self.__dataroot,
                                             transform = transforms.Compose([
                                                 transforms.Resize(self.__img_size),
                                                 transforms.CenterCrop(self.__img_size),
                                                 transforms.ToTensor(),
                                                 transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5)), ]))
        self.__dataloader = torch.utils.data.DataLoader(self.__train_data,
                                                        batch_size = self.__batch_size,
                                                        num_workers = self.__workers)
        self.__ngpu = 1
        # self.__device = torch.device("cpu")
        self.__device = torch.device("cuda")
        self.__ngf = 32
        self.__ndf = 32
        self.__nc = 3
        self.__criterion = nn.BCELoss()

        #self.__OCR = ocr
        #self.__IP = ip
        #self.__CROP_path = crop_path
        #self.__Improvement_path = improvement_path
        self.__curList = []
        self.__coverList = []
        self.__dict_errD = {}

    def showGan(self):
        print("showGan")
        self.__modelG = nn.DataParallel(self.__modelG)
        self.__modelG.cuda()
        self.__modelD = nn.DataParallel(self.__modelD)
        self.__modelD.cuda()
        checkpointG = torch.load('./modelData/ver3_gModel_288_0.pt', map_location=torch.device('cpu'))
        checkpointD = torch.load('./modelData/ver_999_dModel_100_11.pt', map_location=torch.device('cpu'))
        state_dict_G = checkpointG['model_state_dict']
        state_dict_D = checkpointD['model_state_dict']
        new_state_dict_G = OrderedDict()
        new_state_dict_D = OrderedDict()

        for k, v in state_dict_G.items():
            k = 'module._Generator__'+k
            new_state_dict_G[k] = v
        for k, v in state_dict_D.items():
            k = 'module._Discriminator__'+k
            new_state_dict_D[k] = v
        # for k, v in state_dict_D.items():
        #     k = 'module._Generator__'+k
        # new_state_dict_G[k] = v

        self.__modelG.load_state_dict(new_state_dict_G)
        self.__modelD.load_state_dict(new_state_dict_D)

        # self.__modelG.load_state_dict(torch.load('./modelData/ver2_gModel_319_0.pt', map_location='cuda:0'))
        # self.__modelD.load_state_dict(torch.load('./modelData/ver2_dModel_319_0.pt', map_location='cuda:0'))
        self.__modelG.eval()
        self.__modelD.eval()

        predict_list = []

        for i, data in enumerate(self.__dataloader, 0):
            self.__modelD.zero_grad()
            real_cpu = data[0].to(self.__device)
            b_size = real_cpu.size(0)
            label = torch.full((b_size,), 1, device = self.__device)
            output = self.__modelD(real_cpu).view(-1)

            errD_real = self.__criterion(output, label)
            errD_real.backward()
            noise = torch.randn(b_size, 128, 1, 1, device=self.__device)
            fake = self.__modelG(noise)
            label.fill_(0)
            output = self.__modelD(fake.detach()).view(-1)

            errD_fake = self.__criterion(output, label)
            errD_fake.backward()
            errD = errD_real
            self.__dict_errD[self.__train_data_name[i]] = errD.item()
            print(self.__train_data_name[i], errD)
            if errD < 2.3:
                predict_list.append(self.__train_data_name[i])

        self.__coverList = predict_list
        # Perfect_Cover = self.send2OCR(predict_list)
        # print(Perfect_Cover)

    def send2OCR(self, file_List):

        print("OCR에 파일 목록 전송")
        #OCR에 보낸다.
        self.__OCR.crop(file_List)

        crop_list = os.listdir(self.__CROP_path)

        self.__IP.improve(crop_list)

        improvement_list = os.listdir(self.__Improvement_path)
        Perfect_Cover = self.__OCR.comparison(improvement_list)

        print("OCR 결과 받음")
        print(str(len(file_List)) + '중 ' + str(len(Perfect_Cover)) + '개 표지로 확인')

        for i in Perfect_Cover:
            self.__coverList.append(i)

        return Perfect_Cover

    def deleteList(self, curList, resultList):
        for num in range(len(resultList)):
            curList.remove(resultList[num])
        return curList

    def classifying(self, path, num):
        print('-------------------------------')
        print(str(num) + '번째 모델 적용')
        X_test = self.resizeData(path, self.__curList)
        curPredict = self.fitModel(self.__loaded_model, self.__X_train, X_test)
        resultList = self.send2OCR(self.classifyData(curPredict, self.__curList))
        self.__curList = self.deleteList(self.__curList, resultList)
        print('-------------------------------')

    def identify_cover(self):
        return self.__coverList

    def dictErrD(self):
        return self.__dict_errD


if __name__ == '__main__':
    pass
