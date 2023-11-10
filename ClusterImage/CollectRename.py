import os
import shutil
from pathlib import Path

# 获取当前目录
current_dir = Path.cwd()

# 获取当前目录下的所有子目录
sub_dirs = [sub_dir for sub_dir in current_dir.iterdir() if sub_dir.is_dir()]

# 遍历所有子目录
for sub_dir in sub_dirs:
    # 获取子目录中的所有文件
    files = list(sub_dir.glob('*'))
    # 遍历子目录中的所有文件
    for file in files:
        # 如果文件是图片（我们这里假设图片的扩展名为.jpg, .png, .jpeg, .gif）
        if file.suffix in ['.jpg', '.png', '.jpeg', '.gif']:
            # 构建新的文件名，原始文件名后面添加子目录的名称
            new_file_name = f"{file.stem}_{sub_dir.name}{file.suffix}"
            # 构建新的文件路径
            new_file_path = current_dir / new_file_name
            # 移动文件
            shutil.move(str(file), str(new_file_path))

print("All image files have been moved successfully.")