from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox, QHBoxLayout, QSpacerItem, QSizePolicy
from client.main_elements import Customer, User, main_functions
from client.registration import RegisterWindow

class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.mainfunctions = main_functions

        self.setWindowTitle("Авторизация")
        self.setFixedSize(300, 150)  # Фиксированный размер окна

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        layout = QVBoxLayout(self.central_widget)

        self.label_username = QLabel("Логин:", self)
        self.lineEdit_username = QLineEdit(self)

        self.label_password = QLabel("Пароль:", self)
        self.lineEdit_password = QLineEdit(self)
        self.lineEdit_password.setEchoMode(QLineEdit.EchoMode.Password)

        layout.addWidget(self.label_username)
        layout.addWidget(self.lineEdit_username)
        layout.addWidget(self.label_password)
        layout.addWidget(self.lineEdit_password)

        # Промежуток между виджетами
        layout.addSpacing(10)

        button_layout = QHBoxLayout()

        self.button_login = QPushButton("Войти", self)
        self.button_login.clicked.connect(self.login)

        self.button_register = QPushButton("Зарегистрироваться", self)
        self.button_register.clicked.connect(self.open_register_window)

        # Промежуток между кнопками
        button_layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        button_layout.addWidget(self.button_login)
        button_layout.addWidget(self.button_register)
        button_layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))

        layout.addLayout(button_layout)

        # Отображение окна по центру экрана
        self.center()

    def login(self):
        user = self.mainfunctions.login(User(login = self.lineEdit_username.text(), password = self.lineEdit_password.text()))
        if user:
            if user.type_id == 4:
                QMessageBox.information(self, "Успех", "Вы вошли в аккаунт!")
            elif user.type_id == 3:
                QMessageBox.information(self, "Успех", "Вы вошли в аккаунт!")
            elif user.type_id == 2:
                QMessageBox.information(self, "Успех", "Вы вошли в аккаунт!")
            elif user.type_id == 1:
                QMessageBox.information(self, "Успех", "Вы вошли в аккаунт!")
        else: 
            QMessageBox.information(self, "Провал", "Неверный логин или пароль!")

    def open_register_window(self):
        self.hide()  # Скрываем окно авторизации
        self.register_window = RegisterWindow(self)
        self.register_window.show()

    def center(self):
        # Получаем размеры экрана
        screen = QApplication.primaryScreen().geometry()
        # Получаем размеры окна
        size = self.geometry()
        # Позиционируем окно по центру экрана
        self.move((screen.width() - size.width()) // 2, (screen.height() - size.height()) // 2)