import sys
from PyQt6.QtWidgets import QApplication, QDialog, QMessageBox, QPushButton, QVBoxLayout

class CustomDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle('自定义对话框')
        self.layout = QVBoxLayout(self)

        self.next_button = QPushButton('下一步')
        self.next_button.clicked.connect(self.show_next_dialog)

        self.finish_button = QPushButton('完成')
        self.finish_button.clicked.connect(self.close_dialog)

        self.layout.addWidget(self.next_button)
        self.layout.addWidget(self.finish_button)

        self.dialog_counter = 1

    def show_next_dialog(self):
        self.close()
        if self.dialog_counter < 9:
            next_dialog = CustomDialog()
            next_dialog.dialog_counter = self.dialog_counter + 1
            next_dialog.exec()
        else:
            self.close()

    def close_dialog(self):
        self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    dialog = CustomDialog()
    dialog.exec()
    sys.exit(app.exec())