import os

def rename_images(folder_path, total_images, target_image):
    # 获取文件夹内所有文件
    files = os.listdir(folder_path)
    
    # 计数器
    count = 0
    
    # 遍历文件夹内的所有文件
    for file in files:
        # 拼接文件的完整路径
        file_path = os.path.join(folder_path, file)
        
        # 判断文件是否是jpg格式
        if file.lower().endswith('.jpg'):
            # 构造新的文件名
            if count < 23:
                new_name = f"{count}_0.jpg"
            else:
                new_name = f"{count}_1.jpg"
            
            # 构造新的文件路径
            new_path = os.path.join(folder_path, new_name)
            
            # 重命名文件
            os.rename(file_path, new_path)
            
            # 更新计数器
            count += 1

# 指定文件夹路径
folder_path = r"C:\Users\Allan\Desktop\MyFixMATCH\data\lb"

# 设定总共的图片数量和target_image的值
total_images = 45
target_image = 'i'

# 调用函数处理文件夹内的文件
rename_images(folder_path, total_images, target_image)
