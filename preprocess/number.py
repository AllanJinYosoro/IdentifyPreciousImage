import os

# 设置文件夹路径
directory_path = '文件夹路径'

# 获取所有文件
all_files = os.listdir(directory_path)

# 初始化编号
index = 1

# 遍历所有文件
for file in sorted(all_files):
    # 构造文件的新名称，这里只是简单地用数字加上原来的扩展名
    file_extension = os.path.splitext(file)[1]
    new_filename = f"{index}{file_extension}"

    # 拼接完整的文件路径
    old_file_path = os.path.join(directory_path, file)
    new_file_path = os.path.join(directory_path, new_filename)

    # 重命名文件
    os.rename(old_file_path, new_file_path)

    # 更新编号
    index += 1

print(f"Renamed {index - 1} files.")
