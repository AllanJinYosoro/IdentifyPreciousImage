import argparse
import logging
import math
import os
import random
import shutil
import time
from collections import OrderedDict
from sklearn.metrics import accuracy_score, precision_score, recall_score

import numpy as np
import torch
import torch.nn.functional as F
import torch.optim as optim
from torch.optim.lr_scheduler import LambdaLR
from torch.utils.data import DataLoader, RandomSampler, SequentialSampler
from torch.utils.data.distributed import DistributedSampler
from torch.utils.tensorboard import SummaryWriter
from tqdm import tqdm

from dataset.cifar import get_local_data
from utils import AverageMeter, accuracy,pre_rec
from Mytrain import create_model
from torchvision import transforms
from dataset.cifar import LocalDataSet

cifar10_mean = (0.4914, 0.4822, 0.4465)
cifar10_std = (0.2471, 0.2435, 0.2616)

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
        for inputs, labels in test_loader:
            inputs = inputs.to(device)
            labels = labels.to(device)
            
            # forward pass through the model
            outputs = model(inputs)
            
            # convert the outputs to probabilities
            probs = torch.nn.functional.softmax(outputs, dim=1)
            
            all_outputs.append(probs.cpu().numpy())
            all_labels.append(labels.cpu().numpy())
            
    return np.concatenate(all_outputs, axis=0), np.concatenate(all_labels, axis=0)

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

    args = parser.parse_args()

    test_dataloader = get_predict_dataloader(args)

    predictions,predict_labels = predict(args,args.predict_model_path,test_dataloader)

    real_labels = []
    for i, (inputs, targets) in enumerate(test_dataloader):
        real_labels = np.hstack([real_labels,targets])
    
    acc = accuracy_score(real_labels, predict_labels)
    precision = precision_score(real_labels, predict_labels, average='binary')
    recall = recall_score(real_labels, predict_labels, average='binary')

    print(acc,precision,recall)