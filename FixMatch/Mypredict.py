import argparse
import logging
import math
import os
import random
import shutil
import time
from collections import OrderedDict
from sklearn.metrics import accuracy_score, precision_score, recall_score,roc_auc_score, roc_curve,confusion_matrix,f1_score
import matplotlib.pyplot as plt
import plotly.graph_objects as go

import numpy as np
import torch
import torch.nn.functional as F
import torch.optim as optim
from torch.optim.lr_scheduler import LambdaLR
from torch.utils.data import DataLoader, RandomSampler, SequentialSampler
from torch.utils.data.distributed import DistributedSampler
from torch.utils.tensorboard import SummaryWriter
from tqdm import tqdm
from PIL import Image
from torch.utils.data import Dataset

from dataset.cifar import get_local_data
from utils import AverageMeter, accuracy,pre_rec
from Mytrain import create_model
from torchvision import transforms
from dataset.cifar import get_images_and_labels

cifar10_mean = (0.4914, 0.4822, 0.4465)
cifar10_std = (0.2471, 0.2435, 0.2616)

class LocalDataSet(Dataset):
    def __init__(self, dir_path, transform=None):
        self.dir_path = dir_path  # 数据集根目录
        self.transform = transform
        self.images, self.labels = get_images_and_labels(self.dir_path)
 
    def __len__(self):
        return len(self.images)
 
    def __getitem__(self, index):
        img_name= self.images[index]
        img_path=os.path.join(self.dir_path,img_name)

        img = Image.open(img_path)

        img=self.transform(img)
        label = self.labels[index]
        return img, label, img_path  # 返回图像，标签以及图像路径

def get_predict_dataloader(args):
    transfortm_val = transforms.Compose([
        transforms.CenterCrop(size=32),
        transforms.ToTensor(),
        transforms.Normalize(mean=cifar10_mean, std=cifar10_std)
    ])  #验证集的标准化
 
    test_dataset=LocalDataSet(args.predict_data_path,transform=transfortm_val)

    test_loader = DataLoader(
        test_dataset,
        sampler=SequentialSampler(test_dataset),
        batch_size=args.batch_size,
        shuffle=False,
        num_workers=args.num_workers)
 
    return test_loader

def predict(args, model_checkpoint_path, test_loader):
    """
    Predict function for new data using a trained model
    Args:
        args: parsed arguments
        model_checkpoint_path(str): the path of the trained model checkpoint
        test_loader(torch.utils.data.DataLoader): DataLoader for test data
    """
    args.num_classes = 2
    if args.arch == 'wideresnet':
        args.model_depth = 28
        args.model_width = 2
    elif args.arch == 'resnext':
        args.model_cardinality = 4
        args.model_depth = 28
        args.model_width = 4

    # load the saved checkpoint
    checkpoint = torch.load(model_checkpoint_path)
    
    # create the model
    model = create_model(args)
    model.load_state_dict(checkpoint['state_dict'])
    
    # move the model to the device
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = model.to(device)
    
    # set the model to evaluation mode
    model.eval()
    
    all_outputs = []
    all_labels = []
    
    with torch.no_grad():
        for inputs, labels,_ in test_loader:
            inputs = inputs.to(device)
            labels = labels.to(device)
            
            # forward pass through the model
            outputs = model(inputs)
            
            # convert the outputs to probabilities
            probs = torch.nn.functional.softmax(outputs, dim=1)
            
            all_outputs.append(probs.cpu().numpy())
            all_labels.append(labels.cpu().numpy())
            
    return np.concatenate(all_outputs, axis=0), np.concatenate(all_labels, axis=0)

def plot_roc(predict, true):
    # 计算各项指标
    roc_auc = roc_auc_score(true, predict)
    # 计算ROC曲线
    fpr, tpr, _ = roc_curve(true, predict)
    # 可视化ROC曲线
    plt.figure()
    plt.plot(fpr, tpr, color='darkorange', lw=2, label='ROC curve (area = %0.2f)' % roc_auc)
    plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
    plt.xlim([0.0, 1.03])
    plt.ylim([0.0, 1.03])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Receiver Operating Characteristic Curve')
    plt.legend(loc="lower right")
    plt.show()

    return 0

def plot_ConfusionMatrix(true,predict):
    # 计算各个指标
    accuracy = accuracy_score(true, predict)
    precision = precision_score(true, predict)
    recall = recall_score(true, predict)
    f1 = f1_score(true, predict)
    # 计算混淆矩阵
    cm = confusion_matrix(true, predict)
    # 提取TP, TN, FP, FN
    tn, fp, fn, tp = cm.ravel()

    # define the colors: green red blue yellow
    color_grbyo = dict(
        g='rgb(183, 215, 168)',r='rgb(235, 153, 153)',b='rgb(162, 196, 201)',
        y='rgb(255, 229, 154)',o='rgb(239, 127, 89)',w='white'
        )

    fig = go.Figure(data=[go.Table(
        # 列宽
        columnwidth=[30,10,40,40,30,40],
        # 首行
        header=dict(
            # 内容
            values=['','','Actual','','',f'F1 score = {f1:.2f}'],
            # 边框颜色
            line_color='white',
            # 填充颜色
            fill_color=['white','white','white','white','white',color_grbyo['o']],
            # 对齐: 左侧
            align='left',
            # 字体颜色
            font=dict(color=['black','black','black','black','black',color_grbyo['w']],size=12),
            # 行高
            height=30
        ),
        # 后续行
        cells=dict(
            # 内容
            values=list(zip(
                ['','','+','-','',''],
                ['Prediction','+',f'True Positive = {tp}',f'False Positive = {fp}','All Predicted Positive = {}'.format(tp+fp),f'Precision = {precision:.2f}%'],
                ['','-',f'False Negative = {fn}',f'True Negative = {tn}',f'All Predicted Negative = {tn+fn}',''],
                ['','','All Positive Instances = {}'.format(tp+fn),'All Negative Instances = {}'.format(tn+fp),'',''],
                ['' for i in range(6)],
                ['','',f'Recall = {recall:.2f}%','','',f'Accuracy = {accuracy:.2f}%'],
            )),
            # 边框颜色
            line_color='white',
            # 填充色
            fill_color=list(zip(
                ['white','white',color_grbyo['g'],color_grbyo['r'],'white','white'],
                ['white',color_grbyo['g'],color_grbyo['g'],color_grbyo['b'],'white',color_grbyo['o']],
                ['white',color_grbyo['r'],color_grbyo['y'],color_grbyo['r'],'white','white'],
                ['white','white','white','white','white','white'],
                ['white','white','white','white','white','white'],
                ['white','white',color_grbyo['o'],'white','white',color_grbyo['o']]
            )),
            # 对齐: 左侧
            align='left',
            # 字体颜色
            font=dict(
                color=list(zip(
                    ['black' for i in range(6)],
                    ['black','black','black','black','black',color_grbyo['w']],
                    ['black' for i in range(6)],
                    ['black' for i in range(6)],
                    ['black' for i in range(6)],
                    ['black','black',color_grbyo['w'],'black','black',color_grbyo['w']],
                )),
                size=12),
            # 行高
            height=25
        ))
    ])

    fig.show()
    return 0


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='PyTorch FixMatch Training')
    parser.add_argument('--gpu-id', default='0', type=int,
                        help='id(s) for CUDA_VISIBLE_DEVICES')
    parser.add_argument('--num-workers', type=int, default=4,
                        help='number of workers')
    parser.add_argument('--dataset', default='PhotoGraph', type=str,
                        choices=['cifar10', 'cifar100','PhotoGraph'],
                        help='dataset name')
    parser.add_argument('--num-labeled', type=int, default=45,
                        help='number of labeled data')
    parser.add_argument("--expand-labels", action="store_true",
                        help="expand labels to fit eval steps")
    parser.add_argument('--arch', default='wideresnet', type=str,
                        choices=['wideresnet', 'resnext'],
                        help='dataset name')
    parser.add_argument('--total-steps', default=2**20, type=int,
                        help='number of total steps to run')
    parser.add_argument('--eval-step', default=1024, type=int,
                        help='number of eval steps to run')
    parser.add_argument('--start-epoch', default=0, type=int,
                        help='manual epoch number (useful on restarts)')
    parser.add_argument('--batch-size', default=64, type=int,
                        help='train batchsize')
    parser.add_argument('--lr', '--learning-rate', default=0.03, type=float,
                        help='initial learning rate')
    parser.add_argument('--warmup', default=0, type=float,
                        help='warmup epochs (unlabeled data based)')
    parser.add_argument('--wdecay', default=5e-4, type=float,
                        help='weight decay')
    parser.add_argument('--nesterov', action='store_true', default=True,
                        help='use nesterov momentum')
    parser.add_argument('--use-ema', action='store_true', default=True,
                        help='use EMA model')
    parser.add_argument('--ema-decay', default=0.999, type=float,
                        help='EMA decay rate')
    parser.add_argument('--mu', default=7, type=int,
                        help='coefficient of unlabeled batch size')
    parser.add_argument('--lambda-u', default=1, type=float,
                        help='coefficient of unlabeled loss')
    parser.add_argument('--T', default=1, type=float,
                        help='pseudo label temperature')
    parser.add_argument('--threshold', default=0.95, type=float,
                        help='pseudo label threshold')
    parser.add_argument('--out', default='result',
                        help='directory to output the result')
    parser.add_argument('--resume', default='', type=str,
                        help='path to latest checkpoint (default: none)')
    parser.add_argument('--seed', default=None, type=int,
                        help="random seed")
    parser.add_argument("--amp", action="store_true",
                        help="use 16-bit (mixed) precision through NVIDIA apex AMP")
    parser.add_argument("--opt_level", type=str, default="O1",
                        help="apex AMP optimization level selected in ['O0', 'O1', 'O2', and 'O3']."
                        "See details at https://nvidia.github.io/apex/amp.html")
    parser.add_argument("--local_rank", type=int, default=-1,
                        help="For distributed training: local_rank")
    parser.add_argument('--no-progress', action='store_true',
                        help="don't use progress bar")
    parser.add_argument('--predict_model_path',type = str,
                        help = 'Where you store your model to predict')
    parser.add_argument('--predict_data_path',type = str,
                        help = 'Where you store your data to predict')
    parser.add_argument('--user',type = str, default='allan',
                        help = 'username')

    args = parser.parse_args()

    test_dataloader = get_predict_dataloader(args)

    inputs,predict_labels = predict(args,args.predict_model_path,test_dataloader)

    test_pathes,real_labels = [],[]
    for i, (inputs, targets,pathes) in enumerate(test_dataloader):
        test_pathes = np.hstack([test_pathes,pathes])
        real_labels = np.hstack([real_labels,targets])
    #test_pathes是文件地址与predict_labels一一对应
    
    acc = accuracy_score(real_labels, predict_labels)
    precision = precision_score(real_labels, predict_labels, average='binary')
    recall = recall_score(real_labels, predict_labels, average='binary')

    #print(acc,precision,recall)

    plot_roc(predict_labels,real_labels)
    plot_ConfusionMatrix(predict_labels,real_labels)

    # 保存 predict_labels 到文件
    with open(f'UI/data/{args.user}/predict_labels.txt', 'w') as f:
        for item in predict_labels:
            f.write("%s\n" % item)