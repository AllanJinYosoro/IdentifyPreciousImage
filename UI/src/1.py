from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QScrollBar, QSlider, QSpinBox
from PyQt6.QtCore import Qt

class Example(QWidget):
    def __init__(self):
        super().__init__()
        
        self.initUI()
        
    def initUI(self):
        # 创建垂直布局
        layout = QVBoxLayout()
        
        # 创建标签
        self.label = QLabel('参数值: 9', self)
        layout.addWidget(self.label)
        
        # 创建滚动条
        scrollbar = QScrollBar(Qt.Orientation.Horizontal, self)
        scrollbar.valueChanged.connect(self.onScrollBarValueChanged)
        layout.addWidget(scrollbar)
        
        # 创建滑块
        slider = QSlider(Qt.Orientation.Horizontal, self)
        slider.setRange(0, 100)
        slider.setValue(10)
        slider.valueChanged.connect(self.onSliderValueChanged)
        layout.addWidget(slider)
        
        # 创建微调框
        spinbox = QSpinBox(self)
        spinbox.valueChanged.connect(self.onSpinBoxValueChanged)
        layout.addWidget(spinbox)
        
        # 设置布局
        self.setLayout(layout)
        
        # 显示窗口
        self.setWindowTitle('滚动条调节参数示例')
        self.show()
        
    def onScrollBarValueChanged(self, value):
        self.label.setText(f'参数值: {value}')
        
    def onSliderValueChanged(self, value):
        self.label.setText(f'参数值: {value*9}')
        
    def onSpinBoxValueChanged(self, value):
        self.label.setText(f'参数值: {value}')
        
if __name__ == '__main__':
    app = QApplication([])
    ex = Example()
    app.exec()