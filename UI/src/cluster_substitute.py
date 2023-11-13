import os

def get_image_paths(folder_path):
    image_paths = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(('.JPG', '.jpeg', '.png', '.gif')):
                image_path = os.path.join(root, file)
                image_paths.append(image_path)
    return image_paths

folder_path = 'Photos/LPL'  # 替换为实际的文件夹路径
image_paths = get_image_paths(folder_path)

print(image_paths)