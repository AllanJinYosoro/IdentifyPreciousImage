from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QDialog, QFileDialog, QScrollArea, QGridLayout, QWidget, QMessageBox
from PyQt6.QtGui import QPixmap, QIcon, QImage
from PyQt6.QtCore import QSize, Qt, QRunnable, QThreadPool

from global_logger import global_logger
from create_and_remove import create_and_remove, add_replication_suffix, get_all_file_paths
from image import * 
from error_handler import show_error_dialog

import threading
import os

# 创建一个自定义的主窗口类
class MyMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        #设置标题
        self.setWindowTitle('jxh')
        #设置窗口大小
        self.resize(1440,810)


picture_chosen = []

#创建一个对话框类
class CustomMessageBox(QDialog):
    def __init__(self,pictures,picnum,parent=None):
        super().__init__(parent)
        
        # 设置对话框的大小
        self.setMinimumSize(570, 710) 
        self.pictures = pictures
        # 设置背景图片
        #self.setStyleSheet("background-image: url('UI/assets/images/SelectWindow.svg');")
        self.layout = QGridLayout(self)

        # 添加按钮
        self.next_button = QPushButton('下一步')
        self.next_button.clicked.connect(self.show_next_dialog)

        self.icons = self.pictures[9*picnum:9+9*picnum]

        for row in range(3):
            for col in range(3):
                button = QPushButton()
                icon = QIcon(self.icons[row * 3 + col])
                button.setIcon(icon)
                button.setIconSize(QSize(175,175))
                button.setFixedSize(180,180)
                button.setStyleSheet('''
                QPushButton {
                    color: white;
                    border-style: outset;
                    border-width: 2px;
                    border-radius: 10px;
                    border-color: beige;
                    font: bold 14px;
                    }
                QPushButton:pressed {
                    background-color: rgb(100, 100, 100);
                    border-style: inset;
                    }
                QPushButton:disabled {
                    background-color: gray;
                    color: lightgray;
                    border-style: outset;
                    }''')
                button.setProperty("image_path", self.icons[row * 3 + col])
                button.clicked.connect(self.button_click)
                self.layout.addWidget(button, row, col)
        self.layout.addWidget(self.next_button,3,1)

        self.dialog_counter = 1
        
    def button_click(self):
        button = self.sender()  # 获取发送信号的按钮
        button.setStyleSheet("background-color: #A9A9A9; color: #FFFFFF;")  # 设置按钮样式
        image_path = button.property("image_path")  # 获取图片地址属性
        picture_chosen.append(image_path)

    def show_next_dialog(self):
        self.close()
        global picture_chosen 
        if self.dialog_counter < 5: #待增加调参
            try:
                next_dialog = CustomMessageBox(self.pictures,self.dialog_counter)
                next_dialog.dialog_counter = self.dialog_counter + 1
                next_dialog.exec()
            except Exception as e:
                show_error_dialog(str(e))

        else:
            picture_chosen = list(set(picture_chosen))
            picture_not_chosen = [element for element in self.pictures if element not in picture_chosen]
            add_replication_suffix('UI/data/compdata/lb',picture_chosen,'_0')
            add_replication_suffix('UI/data/compdata/lb',picture_not_chosen,'_1')
            picture_chosen.clear()

# 创建应用程序对象
app = QApplication([])

# 创建窗口实例
window = MyMainWindow()

# 设置应用程序图标
icon = QIcon("UI/assets/images/photos.png")
app.setWindowIcon(icon)

# 加载背景图片
background_image = QPixmap("UI/assets/images/background.png")

# 创建一个 QLabel，用于显示背景图片
background_label = QLabel(window)
background_label.setPixmap(background_image)
background_label.setGeometry(0, 0, window.width(), window.height())  # 设置标签大小与窗口大小一致

# 创建按钮
button = QPushButton(window)

button.setFixedSize(60, 60)

# 设置按钮的样式表
button.setStyleSheet("""
    QPushButton {
        border: none;
        background-image: url(UI/assets/images/Vector.svg);
        background-repeat: no-repeat;
        background-position: center;
        padding: 0;
    }
""")

# 设置按钮的初始位置
button.move(4, 48)

# 创建滚动框
scroll_area = QScrollArea(window)
scroll_area.setWidgetResizable(True)

# 创建一个容器窗口
container = QWidget()
scroll_area.setWidget(container)

# 设置滚动区域在主窗口中的大小和位置
scroll_area.setMinimumSize(1300, 690)
scroll_area.setMaximumSize(1300, 690)

scroll_area.setStyleSheet("background-color: transparent;")

# 创建网格布局
grid_layout = QGridLayout(container)

# 创建文件选择按钮
select_folder_button = QPushButton(window)
select_folder_button.setFixedSize(96,32)

# 设置按钮的样式表
select_folder_button.setStyleSheet("""
    QPushButton {
        border: none;
        background-image: url(UI/assets/images/import.svg);
        background-repeat: no-repeat;
        background-position: center;
        padding: 0;
    }
""")

# 定义文件夹路径变量
folder_path = ""

def select_folder():
    global folder_path

    folder_path = QFileDialog.getExistingDirectory(window, "选择文件夹")
    start_background_task(folder_path)
    global_logger.info(folder_path)
    global_logger.info('start cluster')

    if folder_path:
        # 清空之前的图片
        clear_images()

        # 显示文件夹中的图片
        show_images()

def clear_images():
    # 清空网格布局中的图片
    while grid_layout.count():
        item = grid_layout.takeAt(0)
        widget = item.widget()
        widget.deleteLater()

def show_images():
    # 获取文件夹中的所有图片文件路径
    image_paths = [os.path.join(folder_path, file) for file in os.listdir(folder_path) if file.endswith(('.png', '.jpg', '.jpeg', '.JPG'))]

    # 缩放图片的目标大小
    target_size = (220, 150)

    # 将图片添加到网格布局中
    for i, image_path in enumerate(image_paths):
        # 加载原始图片
        image = QImage(image_path)

        # 缩放图片
        scaled_image = image.scaled(*target_size)

        # 创建标签并设置缩放后的图片
        label = QLabel()
        label.setPixmap(QPixmap.fromImage(scaled_image))

        grid_layout.addWidget(label, i // 4, i % 4)  # 每行显示3张图片


# 连接文件选择按钮的点击事件与选择文件夹的函数
select_folder_button.clicked.connect(select_folder)

select_folder_button.move(1060,60)
scroll_area.move(80,120)

# 后台任务函数
def background_task(folder):
    # 后台运行的函数逻辑
    global manage_btn_lock
    manage_btn_lock = True
    create_and_remove(folder,500,50)
    manage_btn_lock = False
    #cluster_pictures = cluster_N_unique_image(folder)
    QMessageBox.information(window,"完成", "标记完成")


def start_background_task(folder):
        # 创建后台线程
        thread = threading.Thread(target=background_task,args = (folder,))
        # 启动后台线程
        thread.start()

# 定义按钮点击事件的槽函数
def button_clicked():
    try:
        # 创建自定义消息框窗口
        msg_box = CustomMessageBox(get_all_file_paths('UI/data/rawdata/lb'),0)
    
        # 显示消息框并等待用户响应
        clicked_button = msg_box.exec()
    except Exception as e:
        show_error_dialog(str(e))

# 将按钮的点击信号连接到槽函数
button.clicked.connect(button_clicked)

# 显示窗口
window.show()

# 启动应用程序的事件循环
app.exec()