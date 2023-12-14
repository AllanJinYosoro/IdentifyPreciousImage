import typing
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QDialog, QFileDialog, QScrollArea, QGridLayout, QWidget, QVBoxLayout, QLineEdit, QMessageBox, QSlider

from PyQt6.QtGui import QPixmap, QIcon, QImage, QFont
from PyQt6.QtCore import QSize

from global_logger import global_logger
from create_and_remove import create_and_remove, add_replication_suffix, get_all_file_paths
from image import * 
from error_handler import show_error_dialog

import threading
import subprocess
import os
import json
import shutil

class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        #设置标题
        self.setWindowTitle('jxh')

        self.user_data = self.load_user_data()

        self.resize(940, 600)
        # 加载背景图片
        self.background_image = QPixmap("UI/assets/images/login.png")

        self.background_label = QLabel(self)
        self.background_label.setPixmap(self.background_image)
        self.background_label.setGeometry(0, 0, self.width(), self.height())  # 设置标签大小与窗口大小一致

        # 设置字体
        self.font = QFont()
        self.font.setPointSize(16)
        # Login widgets
        self.login_username_label = QLabel("Username:",self)
        self.login_username_label.setFont(self.font)
        self.login_username_input = QLineEdit(self)
        self.login_username_input.setFixedSize(250, 50) 
        self.login_username_input.setStyleSheet("""
                QLineEdit {
                    border: 1px solid gray;
                    border-radius: 10px;
                    padding: 0 8px;
                    background: white;
                    selection-background-color: darkgray;
                }
            """)
        self.login_password_label = QLabel("Password:",self)
        self.login_password_label.setFont(self.font)
        self.login_password_input = QLineEdit(self)
        self.login_password_input.setFixedSize(250, 50) 
        self.login_password_input.setStyleSheet("""
                QLineEdit {
                    border: 1px solid gray;
                    border-radius: 10px;
                    padding: 0 8px;
                    background: white;
                    selection-background-color: darkgray;
                }
            """)
        self.login_password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.login_button = QPushButton("Sign in",self)
        self.login_button.setFont(self.font)
        self.login_button.setFixedSize(250, 50)
        self.login_button.setStyleSheet("""
                QPushButton {
                    border: none;
                    border-radius: 10px;
                    background-color: #80C8FF;
                }
            """)
        self.login_button.clicked.connect(self.login)

        self.skip_button = QPushButton('Don\'t have an account? Sign up',self)
        self.skip_button.setFixedSize(250, 50)

        self.skip_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
            }
            QPushButton:hover {
                color: blue;
            }
            QPushButton:pressed {
                color: red;
            }
        """)
        self.skip_button.clicked.connect(self.turn_to_register)

        # Add widgets to window
        self.login_username_label.move(583, 156)
        self.login_username_input.move(583, 196)
        self.login_password_label.move(583, 255)
        self.login_password_input.move(583, 293)
        self.login_button.move(583, 385)
        self.skip_button.move(583, 450)

    def load_user_data(self):
        try:
            with open('UI/user/user_data.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}
        
    def login(self):
        username = self.login_username_input.text()
        password = self.login_password_input.text()
        if  self.user_data.get(username) is not None:
            if self.user_data.get(username)['password'] == password:
                self.main_window = MyMainWindow(self.user_data[username])  # Create a new MyMainWindow
                self.main_window.show()  # Show the main window
                self.close()  # Close the login window
            else:
                QMessageBox.warning(self, "错误", "密码错误！")
        else:
                QMessageBox.warning(self, "错误", "用户名错误！")

    def turn_to_register(self):
        self.register_window = RegisterWindow()
        self.register_window.show()
        self.close()

class RegisterWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        #设置标题
        self.setWindowTitle('jxh')

        self.user_data = self.load_user_data()

        self.resize(940, 600)
        # 加载背景图片
        self.background_image = QPixmap("UI/assets/images/login.png")

        self.background_label = QLabel(self)
        self.background_label.setPixmap(self.background_image)
        self.background_label.setGeometry(0, 0, self.width(), self.height())  # 设置标签大小与窗口大小一致

        # 设置字体
        self.font = QFont()
        self.font.setPointSize(16)  # 设置字体大小为 14
        # Registration widgets
        self.register_username_label = QLabel("Username:",self)
        self.register_username_label.setFont(self.font)
        self.register_username_input = QLineEdit(self)
        self.register_username_input.setFixedSize(250, 50) 
        self.register_username_input.setStyleSheet("""
                QLineEdit {
                    border: 1px solid gray;
                    border-radius: 10px;
                    padding: 0 8px;
                    background: white;
                    selection-background-color: darkgray;
                }
            """)
        self.register_password_label = QLabel("Password:",self)
        self.register_password_label.setFont(self.font)
        self.register_password_input = QLineEdit(self)
        self.register_password_input.setFixedSize(250, 50) 
        self.register_password_input.setStyleSheet("""
                QLineEdit {
                    border: 1px solid gray;
                    border-radius: 10px;
                    padding: 0 8px;
                    background: white;
                    selection-background-color: darkgray;
                }
            """)
        self.register_password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.register_button = QPushButton("Sign up",self)
        self.register_button.setFont(self.font)
        self.register_button.setFixedSize(250, 50)
        self.register_button.setStyleSheet("""
                QPushButton {
                    border: none;
                    border-radius: 10px;
                    background-color: #80C8FF;
                }
            """)
        self.register_button.clicked.connect(self.register)

        self.skip_button = QPushButton('Already a member? Sign in',self)
        self.skip_button.setFixedSize(250, 50)

        self.skip_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
            }
            QPushButton:hover {
                color: blue;
            }
            QPushButton:pressed {
                color: red;
            }
        """)
        self.skip_button.clicked.connect(self.turn_to_login)

        # Add widgets to window
        self.register_username_label.move(583, 156)
        self.register_username_input.move(583, 196)
        self.register_password_label.move(583, 255)
        self.register_password_input.move(583, 293)
        self.register_button.move(583, 385)
        self.skip_button.move(583, 450)


    def load_user_data(self):
        try:
            with open('UI/user/user_data.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def save_user_data(self):
        with open('UI/user/user_data.json', 'w') as f:
            json.dump(self.user_data, f)

    def register(self):
        username = self.register_username_input.text()
        password = self.register_password_input.text()

        if username in self.user_data:
            QMessageBox.warning(self, "错误", "用户名已存在！")
        elif not username or not password:
            QMessageBox.warning(self, "错误", "用户名或密码不能为空！")
        else:
            self.user_data[username] = {'username': username, 'password': password, 'parameters': [45,45], 'model': 'Not completed'}
            self.save_user_data()
            QMessageBox.information(self, "成功", "注册成功！")
            self.login_window = LoginWindow()  # Create a new LoginWindow
            self.login_window.show()
            self.close()  # Close the register window

    def turn_to_login(self):
        self.login_window = LoginWindow()
        self.login_window.show()
        self.close()

class Userwindow(QWidget):
    def __init__(self,user,mainwindow):
        super().__init__() 
        self.resize(60, 140)
        
        self.avatar_button = QPushButton(self)
        self.avatar_button.setFixedSize(40, 40)
        self.avatar_button.move(10, 10)
        self.user = user
        self.username = user['username']
        self.mainwindow = mainwindow

        self.avatar_button.clicked.connect(self.set_avatar)
        self.avatar_filename = f"UI/user/avatar/{self.username}.png"
        if not os.path.exists(self.avatar_filename):
            self.avatar_filename = "UI/assets/images/noavatar.jpg"
        self.set_avatar_pixmap()

        self.profile_button = QPushButton(self)
        self.profile_button.setFixedSize(60, 30)
        self.profile_button.move(0, 60)
        self.profile_button.setText('profile')
        self.profile_button.clicked.connect(self.show_profile)

        self.sign_out_button = QPushButton(self)
        self.sign_out_button.setFixedSize(60, 30)
        self.sign_out_button.move(0, 90)
        self.sign_out_button.setText('sign out')
        self.sign_out_button.clicked.connect(self.sign_out)

    def set_avatar_pixmap(self):
        self.avatar_pixmap = QPixmap(self.avatar_filename)
        self.avatar_icon = QIcon(self.avatar_pixmap)
        self.avatar_button.setIcon(self.avatar_icon)
        self.avatar_button.setIconSize(QSize(40,40))  # Set the size of the avatar button to match the image

    def set_avatar(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Select Avatar", "",
                                              "Images (*.png *.jpeg *.jpg *.bmp *.gif)")
        if filename:
            if not os.path.exists("UI/user/avatar"):
                os.makedirs("UI/user/avatar")
            avatar_path = f"UI/user/avatar/{self.username}.png"
            shutil.copyfile(filename, avatar_path)  # copy the selected file to user/avatar directory
            self.avatar_filename = avatar_path
            self.set_avatar_pixmap()

    def show_profile(self):
        self.profile_window = ProfileWindow(self.user)
        self.profile_window.show()
        self.close()
        self.mainwindow.close()

    def sign_out(self):
        self.mainwindow.close()
        self.login_window = LoginWindow()
        self.login_window.show()

class ProfileWindow(QMainWindow):
    def __init__(self,user):
        super().__init__()
        self.user = user
        self.user_name = self.user['username']
        self.parameters = self.user['parameters']
        self.user_model = self.user['model']

        self.resize(1440, 810)
        # 加载背景图片
        self.background_image = QPixmap("UI/assets/images/background.png")

        self.background_label = QLabel(self)
        self.background_label.setPixmap(self.background_image)
        self.background_label.setGeometry(0, 0, self.width(), self.height())

        self.back_btn = 

        self.username_label = QLabel(f'username',self)
        self.username_label.setFont(QFont('Arial', 40))
        self.username_label.move(380, 190)

        self.label_number = QLabel(f'Number of labelled pictures: {self.parameters[0]}', self)
        self.label_number.setFont(QFont('Arial', 32))
        self.label_number.move(190, 360)

        self.test_number = QLabel(f'Number of test pictures: {self.parameters[1]}', self)
        self.test_number.setFont(QFont('Arial', 32))
        self.test_number.move(190, 470)

        self.model_status = QLabel('Model status:', self)
        self.model_status.setFont(QFont('Arial', 32))
        self.model_status.move(190, 580)

        self.if_model = QLabel(f'{self.user_model}', self)
        self.if_model.setFont(QFont('Arial', 32))
        self.if_model.move(800, 580)

        # 创建滑块
        self.label_slider = QSlider(Qt.Orientation.Horizontal, self)
        self.label_slider.setRange(0, 100)
        self.label_slider.setValue((self.parameters[0]/9))
        self.label_slider.move(800, 360)
        self.label_slider.setFixedSize(480,30)
        self.label_slider.valueChanged.connect(self.LabelValueChanged)

        self.test_slider = QSlider(Qt.Orientation.Horizontal, self)
        self.test_slider.setRange(0, 100)
        self.test_slider.setValue((self.parameters[1]/9))
        self.test_slider.move(800, 470)
        self.test_slider.setFixedSize(480,30)
        self.test_slider.valueChanged.connect(self.TestValueChanged)

    def LabelValueChanged(self, value):
        self.label_number.setText(f'Number of labelled pictures: {value*9}')
        self.parameters[0] = value*9
        self.user['parameters'] = self.parameters

    def TestValueChanged(self, value):
        self.test_number.setText(f'Number of test pictures: {value*9}')
        self.parameters[1] = value*9
        self.user['parameters'] = self.parameters

    def save_user_data(self):
        with open('UI/user/user_data.json', 'r') as f:
                self.data_to_dump = json.load(f)

        self.data_to_dump[self.user_name] = self.user
        with open('UI/user/user_data.json', 'w') as f:
            json.dump(self.data_to_dump, f)


class DialogueWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("setting")

        # 创建一个布局
        layout = QVBoxLayout(self)

        # 创建第一个输入框标签和输入框
        label1 = QLabel("label组数(9个一组):")
        layout.addWidget(label1)

        self.input_field1 = QLineEdit()
        layout.addWidget(self.input_field1)

        # 创建第二个输入框标签和输入框
        label2 = QLabel("test组数(9个一组):")
        layout.addWidget(label2)

        self.input_field2 = QLineEdit()
        layout.addWidget(self.input_field2)

        self.button = QPushButton("提交")
        layout.addWidget(self.button)

        # 连接按钮的点击事件到槽函数
        self.button.clicked.connect(self.accept)

#创建一个对话框类
class delete_dialog(QDialog):
    def __init__(self,username,parent=None):
        super().__init__(parent)
        
        # 设置对话框的大小
        self.setMinimumSize(500, 250) 
        self.username = username

        self.renew_button = QPushButton('更新模型')
        self.renew_button.clicked.connect(self.update_btn_clicked)

        self.apply_button = QPushButton('应用模型')
        self.apply_button.clicked.connect(self.apply_btn_clicked)

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.renew_button)
        self.layout.addWidget(self.apply_button)

        self.test_path = []
        self.predict_label = []

    def update_btn_clicked(self):
        self.close()
        self.train()

    def apply_btn_clicked(self):
        self.close()
        self.delete()

    def train(self):
        command = ['python', 'FixMatch/Mytrain.py', '--num-workers', '4', '--dataset', 'PhotoGraph', '--batch-size', '9', '--num-labeled', '45', '--eval-step', '1024', '--total-steps', '204800', '--arch', 'wideresnet', '--lr', '0.03', '--expand-labels', '--seed', '5', '--out', f'UI/assets/models/{self.username}_model']

        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()

        if process.returncode != 0:
            print(f'Error occurred: {stderr.decode()}')
        else:
            print(f'Success! Output: {stdout.decode()}')
    
    def delete(self):
        command = ['python', 'FixMatch/Mypredict.py', '--num-workers', '4', '--dataset', 'PhotoGraph', '--batch-size', '9', '--num-labeled', '45', '--eval-step', '1024', '--total-steps', '204800', '--arch', 'wideresnet', '--lr', '0.03', '--expand-labels', '--seed', '5', '--out', f'UI/assets/models/{self.username}_model', '--predict_model_path', f'UI/assets/models/{self.username}_model/checkpoint.pth.tar', '--predict_data_path', 'UI/data/compdata/all']

        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        # 分割子进程的输出
        outputs = process.stdout.splitlines()

        self.test_path = outputs[0].decode()
        self.predict_label = outputs[1].decode()

        if process.returncode != 0:
            print(f'Error occurred: {stderr.decode()}')
        else:
            print(f'Success! Output: {stdout.decode()}')


#创建一个对话框类
class CustomMessageBox(QDialog):
    def __init__(self,pictures,target_folder,picnum,picture_chosen,parent=None):
        super().__init__(parent)
        
        # 设置对话框的大小
        self.setMinimumSize(570, 710) 
        self.pictures = pictures
        self.picture_chosen = picture_chosen
        self.target_folder = target_folder
        self.group_num = (len(pictures)//9)

        # 设置背景图片
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
        self.picture_chosen.append(image_path)


    def show_next_dialog(self):
        self.close()

        if self.dialog_counter < self.group_num: 
            try:
                next_dialog = CustomMessageBox(self.pictures,self.target_folder,self.dialog_counter,self.picture_chosen)
                next_dialog.dialog_counter = self.dialog_counter + 1
                next_dialog.exec()
            except Exception as e:
                show_error_dialog(str(e))

        else:
            self.picture_chosen = list(set(self.picture_chosen))
            self.picture_not_chosen = [element for element in self.pictures if element not in self.picture_chosen]
            add_replication_suffix(self.target_folder,self.picture_chosen,'_0')
            add_replication_suffix(self.target_folder,self.picture_not_chosen,'_1')
            self.picture_chosen.clear()
            

# 创建一个自定义的主窗口类
class MyMainWindow(QMainWindow):
    def __init__(self,user=None):
        super().__init__()

        #设置标题
        self.setWindowTitle('jxh')
        #设置窗口大小
        self.resize(1440,810)

        self.user = user
        self.username = user['username']

        # 加载背景图片
        self.background_image = QPixmap("UI/assets/images/background.png")

        self.background_label = QLabel(self)
        self.background_label.setPixmap(self.background_image)
        self.background_label.setGeometry(0, 0, self.width(), self.height())  # 设置标签大小与窗口大小一致

        # manage按钮
        self.manage_btn = QPushButton(self)
        self.manage_btn.setFixedSize(60, 60)

        # 设置按钮的样式表
        self.manage_btn.setStyleSheet("""
            QPushButton {
                border: none;
                background-image: url(UI/assets/images/manage.svg);
                background-repeat: no-repeat;
                background-position: center;
                padding: 0;
            }
        """)

        # 设置按钮的初始位置
        self.manage_btn.move(4, 48)

        # 将按钮的点击信号连接到槽函数
        self.manage_btn.clicked.connect(self.manage_btn_clicked)

        # test按钮
        self.test_btn = QPushButton(self)
        self.test_btn.setFixedSize(60, 60)

        # 设置按钮的样式表
        self.test_btn.setStyleSheet("""
            QPushButton {
                border: none;
                background-image: url(UI/assets/images/test.svg);
                background-repeat: no-repeat;
                background-position: center;
                padding: 0;
            }
        """)

        self.test_btn.move(4, 120)

        # 将按钮的点击信号连接到槽函数
        self.test_btn.clicked.connect(self.test_btn_clicked)

                # test按钮
        self.setting_btn = QPushButton(self)
        self.setting_btn.setFixedSize(60, 60)

        # 设置按钮的样式表
        self.setting_btn.setStyleSheet("""
            QPushButton {
                border: none;
                background-image: url(UI/assets/images/setting.svg);
                background-repeat: no-repeat;
                background-position: center;
                padding: 0;
            }
        """)

        self.setting_btn.move(4, 192)

        # 将按钮的点击信号连接到槽函数
        self.setting_btn.clicked.connect(self.setting_btn_clicked)

        # 创建滚动框
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)

        # 创建一个容器窗口
        self.container = QWidget()
        self.scroll_area.setWidget(self.container)

        # 设置滚动区域在主窗口中的大小和位置
        self.scroll_area.setMinimumSize(1300, 690)
        self.scroll_area.setMaximumSize(1300, 690)

        self.scroll_area.setStyleSheet("background-color: transparent;")

        # 创建网格布局
        self.grid_layout = QGridLayout(self.container)

        # 创建文件选择按钮
        self.select_folder_btn = QPushButton(self)
        self.select_folder_btn.setFixedSize(96,32)

        # 设置按钮的样式表
        self.select_folder_btn.setStyleSheet("""
            QPushButton {
                border: none;
                background-image: url(UI/assets/images/import.svg);
                background-repeat: no-repeat;
                background-position: center;
                padding: 0;
            }
        """)


        # 连接文件选择按钮的点击事件与选择文件夹的函数
        self.select_folder_btn.clicked.connect(self.select_folder)

        self.select_folder_btn.move(1060,60)
        self.scroll_area.move(80,120)

        self.user_button = QPushButton(self)
        self.user_button.setFixedSize(40, 40)
        self.user_button.move(1150, 2)
        self.user_button.clicked.connect(self.user_window)
        self.avatar_filename = f"UI/user/avatar/{self.username}.png"
        if not os.path.exists(self.avatar_filename):
            self.avatar_filename = "UI/assets/images/noavatar.jpg"
        self.set_avatar_pixmap()

        self.delete_button = QPushButton(self)
        self.delete_button.setFixedSize(60, 60)
        self.delete_button.setStyleSheet("""
            QPushButton {
                border: none;
                background-image: url(UI/assets/images/delete.svg);
                background-repeat: no-repeat;
                background-position: center;
                padding: 0;
            }
        """)

        self.delete_button.move(4, 264)

        self.delete_button.clicked.connect(self.delete_btn_clicked)
        
        # 定义文件夹路径变量
        self.folder_path = ""
        self.picture_chosen = []
        self.manage_btn_available = False
        self.lb_num = 45
        self.test_num = 198
        self.ulb_num = 500

    def select_folder(self):
        self.folder_path = QFileDialog.getExistingDirectory(None, "选择文件夹", "/")

        if self.folder_path:
            self.start_background_task(self.folder_path)
            global_logger.info(self.folder_path)
            global_logger.info('start cluster')

        if self.folder_path:
            # 清空之前的图片
            self.clear_images()

            # 显示文件夹中的图片
            self.show_images()

    def clear_images(self):
        # 清空网格布局中的图片
        while self.grid_layout.count():
            item = self.grid_layout.takeAt(0)
            widget = item.widget()
            widget.deleteLater()

    def show_images(self):
        # 获取文件夹中的所有图片文件路径
        image_paths = [os.path.join(self.folder_path, file) for file in os.listdir(self.folder_path) if file.endswith(('.png', '.jpg', '.jpeg', '.JPG'))]

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

            self.grid_layout.addWidget(label, i // 4, i % 4)  # 每行显示3张图片


    # 后台任务函数
    def background_task(self,folder):
        # 后台运行的函数逻辑
        self.manage_btn_available = False
        create_and_remove(folder,self.lb_num,self.ulb_num,self.test_num)
        self.manage_btn_available = True
        

    def start_background_task(self,folder):
            # 创建后台线程
            thread = threading.Thread(target=self.background_task,args = (folder,))
            # 启动后台线程
            thread.start()

    # 定义按钮点击事件的槽函数
    def manage_btn_clicked(self):
        if self.manage_btn_available:    
            try:
                # 创建自定义消息框窗口
                msg_box = CustomMessageBox(get_all_file_paths('UI/data/rawdata/lb'),'UI/data/compdata/lb',0,[])
            
                # 显示消息框并等待用户响应
                msg_box.exec()
            except Exception as e:
                show_error_dialog(str(e))
        else:
            show_error_dialog('正在归档，请稍后再试')

    def test_btn_clicked(self):
        if self.manage_btn_available:    
            try:
                # 创建自定义消息框窗口
                msg_box = CustomMessageBox(get_all_file_paths('UI/data/rawdata/test'),'UI/data/compdata/test',0,[])
            
                # 显示消息框并等待用户响应
                msg_box.exec()
            except Exception as e:
                show_error_dialog(str(e))
        else:
            show_error_dialog('正在归档，请稍后再试')

    def setting_btn_clicked(self):
        dialogue_window = DialogueWindow(self)
        if dialogue_window.exec() == QDialog.DialogCode.Accepted:
            input_text1 = dialogue_window.input_field1.text()
            input_text2 = dialogue_window.input_field2.text()
            self.lb_num = int(input_text1)*9
            self.test_num = int(input_text2)*9

    def delete_btn_clicked(self):
        delete_dialogue_window = delete_dialog(self.username,self)
        delete_dialogue_window.exec()
        self.test_path = delete_dialogue_window.test_path
        self.predict_label = delete_dialogue_window.predict_label

    def set_avatar_pixmap(self):
        self.avatar_pixmap = QPixmap(self.avatar_filename)
        self.avatar_icon = QIcon(self.avatar_pixmap)
        self.user_button.setIcon(self.avatar_icon)
        self.user_button.setIconSize(QSize(40,40))  # Set the size of the avatar button to match the image

    def user_window(self):
        self.user_window = Userwindow(self.user,self)
        self.user_window.move(1150, 2)
        self.user_window.show()

        

def main():
    # 创建应用程序对象
    app = QApplication([])

    # 创建窗口实例
    register_window = RegisterWindow()
    
    # 设置应用程序图标
    icon = QIcon("UI/assets/images/photos.png")
    app.setWindowIcon(icon)

    # 显示窗口
    register_window.show()

    # 启动应用程序的事件循环
    app.exec()

if __name__ == "__main__":
    main()