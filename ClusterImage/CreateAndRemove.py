import os
import shutil
import random
from pathlib import Path

def CreateAndRemove(pending_label_images,ulb_num,test_num):
    # 定义rawdata目录
    rawdata_dir = Path.cwd() / 'rawdata'

    # 待处理的图片列表
    pending_label_images = pending_label_images  # 这里填入你的图片路径列表

    # 创建子目录
    lb_dir = rawdata_dir / 'lb'
    if not os.path.exists(lb_dir):lb_dir.mkdir(exist_ok=True)

    ulb_dir = rawdata_dir / 'ulb'
    if not os.path.exists(ulb_dir):ulb_dir.mkdir(exist_ok=True)

    test_dir = rawdata_dir / 'test'
    if not os.path.exists(test_dir):test_dir.mkdir(exist_ok=True)

    # 移动图片到lb子目录
    for img_path in pending_label_images:
        img = Path(img_path)
        shutil.move(str(img), str(lb_dir / img.name))

    # 获取rawdata目录下的所有图片文件
    all_images = list(rawdata_dir.glob("*.[jp][np][g]*"))  # 匹配.jpg, .jpeg, .png, .gif等图片文件
    all_images = [img for img in all_images if str(img) not in pending_label_images]  # 剔除已处理的图片

    # 随机选择500张图片移动到ulb子目录
    for img in random.sample(all_images, ulb_num):
        shutil.move(str(img), str(ulb_dir / img.name))
        all_images.remove(img)  # 从列表中移除已处理的图片

    # 随机选择50张图片移动到test子目录
    for img in random.sample(all_images, test_num):
        shutil.move(str(img), str(test_dir / img.name))

    print("All image files have been moved successfully.")