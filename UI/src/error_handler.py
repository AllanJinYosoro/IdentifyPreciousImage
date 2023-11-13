from PyQt6.QtWidgets import QMessageBox

def show_error_dialog(message):
    error_dialog = QMessageBox()
    error_dialog.setIcon(QMessageBox.Icon.Critical)
    error_dialog.setWindowTitle('错误')
    error_dialog.setText(message)
    error_dialog.exec()