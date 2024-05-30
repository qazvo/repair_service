from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QFormLayout, QMessageBox
from PyQt6.QtCore import Qt
from client.main_elements import User, main_functions

class MasterWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Мастер по ремонту")
        self.setFixedSize(300, 200)
        # Добавьте элементы и виджеты, необходимые для мастера