import os
from PIL import Image, ImageOps
import shutil

def compress_image(input_path, output_path, target_size_kb, quality_step):
    """
    将图片压缩至接近指定的大小。
    
    :param input_path: 输入图片的路径
    :param output_path: 输出图片的路径
    :param target_size_kb: 目标大小(KB)
    :param quality_step: 质量调整的步长
    """
    # 打开图片
    with Image.open(input_path) as img:
        # 计算目标大小（字节）
        target_size_bytes = target_size_kb * 1024
        
        # 估算初始质量参数
        quality = 4
        while True:
            # 调整图片大小
            img.save(output_path, quality=quality, optimize=True)
            
            # 如果文件大小接近目标大小或质量低于步长，则停止
            if os.path.getsize(output_path) <= target_size_bytes or quality <= quality_step:
                break
            
            # 减少图片质量
            quality -= quality_step
        
        # 如果文件仍然太大，继续调整分辨率
        while os.path.getsize(output_path) > target_size_bytes:
            with Image.open(output_path) as img:
                # 减少图片的宽度和高度
                img = img.resize((int(img.width * 0.9), int(img.height * 0.9)), Image.Resampling.LANCZOS)
                
                # 再次尝试保存图片
                img.save(output_path, quality=quality, optimize=True)

def compress_images(input_folder,output_folder, target_size_kb=4, quality_step=1):

    # 确保输出文件夹存在
    shutil.rmtree(output_folder)
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 遍历指定文件夹中的所有文件
    for filename in os.listdir(input_folder):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
            # 图片完整路径
            image_path = os.path.join(input_folder, filename)
            
            # 图片的输出路径
            output_path = os.path.join(output_folder, filename)
            
            # 调用压缩函数
            compress_image(image_path, output_path, target_size_kb, quality_step)
