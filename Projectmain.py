import os
import argparse
from preprocess.compress import compress_images
from preprocess.convert_format import convert_format
from ClusterImage.cluster import cluster_N_unique_image
from ClusterImage.CreateAndRemove import CreateAndRemove


parser = argparse.ArgumentParser(description='IdentifyPreciousImage')
parser.add_argument('--raw_data_path', default='./rawdata', type=str,
                        help='The path to unpreprocessed and unclustered data')
parser.add_argument('--cluster_number',type=int,default=45,
                    help="The number of cluster results(lb samples)")
parser.add_argument('--ulb_number',type=int,default=500,
                    help="The number of ulb samples")
parser.add_argument('--test_number',type=int,default=50,
                    help="The number of test samples")
args = parser.parse_args()

if not os.path.exists('./ClusterImage/rawdata'):
    os.mkdir('./ClusterImage/rawdata')
cluster_path = './ClusterImage/rawdata'

#转化为jpg并且编号
convert_format(args.raw_data_path)
#压缩图片
compress_images(args.raw_data_path,cluster_path, target_size_kb=4, quality_step=1)

#cluster
uniqueImage_path = cluster_N_unique_image(args.cluster_number)
#把lb，ulb，test文件夹分别放到各个文件夹内
CreateAndRemove(uniqueImage_path,args.ulb_number,args.test_number)
