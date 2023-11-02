import logging
import math
import os
import torch
import pandas as pd

import numpy as np
from PIL import Image
from torchvision import datasets
from torch.utils.data import Dataset
from torchvision import transforms

from .randaugment import RandAugmentMC

logger = logging.getLogger(__name__)

def GetPhotoGraph(args, root):

    padding = 32

    means,stds = pixelCal()

    transform_labeled = transforms.Compose([
        transforms.RandomHorizontalFlip(),
        transforms.RandomCrop(size=32,
                              padding=int(padding*0.125),
                              padding_mode='reflect'),
        transforms.ToTensor(),
        transforms.Normalize(mean=means, std=stds)
    ])
    transform_val = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize(mean=means, std=stds)
    ])
    
    train_labeled_dataset = read_in_local_graph('train_labeled',transform_labeled,labeled=True)
    
    train_unlabeled_dataset = read_in_local_graph('train_unlabeled',TransformFixMatch(mean=means, std=stds))
    
    test_dataset = read_in_local_graph('test',transform_val)

    return train_labeled_dataset, train_unlabeled_dataset, test_dataset

def pixelCal():
    folder_path = ['./data/train/labeled','./data/test','./data/train/unlabeled']
    images = [[os.path.join(folder,file) for file in os.listdir(folder) if file.endswith('.jpg')] for folder in folder_path]
    image_files = images[0]+images[1]+images[2]

    channel = []

    for image_file in image_files:
        
        # 使用PIL库打开图片
        image = Image.open(image_file)
        
        # 将图片转换为NumPy数组
        image_array = np.array(image)
        
        # 累积每个通道的像素值之和
        channel.append(np.average(image_array, axis=(0, 1)))

    channel = np.vstack(channel).T
    means = np.average(channel,axis=(1))
    stds = np.std(channel,axis=(1))

    return means,np.array([1,1,1])#stds

def read_in_local_graph(istrain_labeled,transform,labeled=False):

    if istrain_labeled == 'train_labeled':
        folder_path = r'./data/train/labeled'
    elif istrain_labeled == 'train_unlabeled':
        folder_path = r'./data/train/unlabeled'
    elif istrain_labeled == 'test':
        folder_path = r'./data/test'

    image_files = [file for file in os.listdir(folder_path) if file.endswith('.jpg')]

    if labeled:
        tag_data = pd.read_csv('./data/train/labeled/tag.csv')
        #tensor_images = []
        image_with_tag = []
        for image_file in image_files:
            image_path = os.path.join(folder_path, image_file)
            image = Image.open(image_path)
            tensor_image = transform(image)
            #tensor_images.append(tensor_image)
            tag = tag_data[tag_data['name'] == image_file].values[:,1]
            image_with_tag.append((tensor_image,tag))
            labeled_dataset = MyDataset(image_with_tag)
        return labeled_dataset
    else:
        tensor_images = []
        for image_file in image_files:
            # 构建完整的图片路径
            image_path = os.path.join(folder_path, image_file)
            # 使用PIL库打开图片
            image = Image.open(image_path)
            # 进行数据转换
            tensor_image = transform(image)
            # 将转换后的 Tensor 对象添加到列表中
            tensor_images.append(tensor_image)
        # 将列表转换为 PyTorch Tensor
        
        print(tensor_images[0][0])
        print('-'*20)
        print(tensor_images[0][1])
        print(folder_path)
        tensor_images = torch.stack(tensor_images)
        unlabeled_dataset = MyDataset(tensor_images)
        return unlabeled_dataset

class TransformFixMatch(object):
    def __init__(self, mean, std):
        self.weak = transforms.Compose([
            transforms.RandomHorizontalFlip(),
            transforms.RandomCrop(size=32,
                                  padding=int(32*0.125),
                                  padding_mode='reflect')])
        self.strong = transforms.Compose([
            transforms.RandomHorizontalFlip(),
            transforms.RandomCrop(size=32,
                                  padding=int(32*0.125),
                                  padding_mode='reflect'),
            RandAugmentMC(n=2, m=10)])
        self.normalize = transforms.Compose([
            transforms.ToTensor(),
            transforms.Normalize(mean=mean, std=std)])

    def __call__(self, x):
        weak = self.weak(x)
        strong = self.strong(x)
        return self.normalize(weak), self.normalize(strong)


class MyDataset(Dataset):
    def __init__(self,data=None):
        self.x = data
    def __getitem__(self, index):
        return self.x[index]
    def __len__(self):
        return len(self.x)