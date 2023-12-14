import os
import shutil
import random
from pathlib import Path
from cluster import cluster_N_unique_image
from compress import compress_images

def generate_file_list(folder_path, path_list):
    folder_path = Path(folder_path)
    file_list = []
    
    for path in path_list:
        file_path = folder_path / Path(path).name
        file_list.append(str(file_path))
    
    return file_list

def get_all_file_paths(folder_path):
    file_paths = []
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            file_paths.append(file_path)
    return file_paths

def rename_images(folder_path, new_filename_prefix):
    # 遍历文件夹中的所有文件
    for index, filename in enumerate(os.listdir(folder_path)):
        if filename.endswith('.jpg') or filename.endswith('.png'):
            # 构建原始文件的完整路径
            original_file = os.path.join(folder_path, filename)

            # 构建新的文件名
            new_filename = f"{new_filename_prefix}_{index+1}{'.jpg'}"

            # 构建新文件的完整路径
            new_file = os.path.join(folder_path, new_filename)

            # 重命名文件
            os.rename(original_file, new_file)

def create_and_remove(src_folder,cluster_num,ulb_num,test_num,user):
    # 定义target_dir目录
    target_dir = Path(f'UI/data/{user}/rawdata')
    compress_images(src_folder,f'UI/data/{user}/compdata/all')

    cluster_result = cluster_N_unique_image(f'UI/data/{user}/compdata/all',cluster_num)# 聚类图片列表

    cluster_result = generate_file_list(src_folder,cluster_result)

    #删除'UI/data/compdata/all'
    shutil.rmtree(f'UI/data/{user}/compdata/all')

    src_folder = Path(src_folder) 
    os.makedirs(f'UI/data/{user}/rawdata')

    # 创建子目录
    lb_dir = target_dir / 'lb'
    if os.path.exists(lb_dir):
        shutil.rmtree(lb_dir)
    if not os.path.exists(lb_dir):lb_dir.mkdir(exist_ok=True)

    ulb_dir = target_dir / 'ulb'
    if os.path.exists(ulb_dir):
        shutil.rmtree(ulb_dir)
    if not os.path.exists(ulb_dir):ulb_dir.mkdir(exist_ok=True)

    test_dir = target_dir / 'test'
    if os.path.exists(test_dir):
        shutil.rmtree(test_dir)
    if not os.path.exists(test_dir):test_dir.mkdir(exist_ok=True)

    # 移动聚类结果到lb子目录
    for img_path in cluster_result:
        img = Path(img_path)
        shutil.copy(str(img), str(lb_dir))
    
    #获取lb子目录下的图片数量
    lb_num = len(list(lb_dir.glob("*.[jp][np][g]*")))
    if lb_num < cluster_num:
        print('lb图片数量不足')
        #复制lb子目录下的图片，直到数量达到45
        for img in random.sample(list(lb_dir.glob("*.[jp][np][g]*")), cluster_num-lb_num):
            shutil.copy(str(img), str(lb_dir/ f'new_{img.name}'))

    # 获取src_folder目录下的所有图片文件
    all_images = list(src_folder.glob("*.[jp][np][g]*"))  # 匹配.jpg, .jpeg, .png, .gif等图片文件
    all_images = [img for img in all_images if str(img) not in cluster_result]  # 剔除已处理的图片

    # 随机选择ulb_num张图片复制到ulb子目录
    for img in random.sample(all_images, ulb_num):
        shutil.copy(str(img), str(ulb_dir))
        all_images.remove(img)  # 从列表中移除已处理的图片

    # 随机选择test_num张图片复制到test子目录
    for img in random.sample(all_images, test_num):
        shutil.copy(str(img), str(test_dir / img.name))

    rename_images(f'UI/data/{user}/rawdata/lb','lb')
    rename_images(f'UI/data/{user}/rawdata/ulb','ulb')
    rename_images(f'UI/data/{user}/rawdata/test','test')
    compress_images(f'UI/data/{user}/rawdata/lb','UI/data/compdata/lb')
    compress_images(f'UI/data/{user}/rawdata/ulb','UI/data/compdata/ulb')
    compress_images(f'UI/data/{user}/rawdata/test','UI/data/compdata/test')

    print('completed')

def add_replication_suffix(target_folder,file_list, suffix):
    for file_path in file_list:
        # 拆分文件路径和文件名
        _, filename = os.path.split(file_path)

        target_path = os.path.join(target_folder, filename)
        # 拆分文件名和扩展名
        name, extension = os.path.splitext(filename)

        # 构建新的文件名
        new_filename = name + suffix + extension

        # 构建新文件的完整路径
        new_file_path = os.path.join(target_folder, new_filename)

        # 重命名文件
        os.rename(target_path, new_file_path)

