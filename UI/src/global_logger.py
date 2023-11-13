import logging

# 创建全局日志记录器
global_logger = logging.getLogger('my_app')
global_logger.setLevel(logging.INFO)

# 创建文件处理器
file_handler = logging.FileHandler('UI/log/app.log')
file_handler.setLevel(logging.INFO)

# 创建日志格式器
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

# 将文件处理器添加到全局日志记录器
global_logger.addHandler(file_handler)