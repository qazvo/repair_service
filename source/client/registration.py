from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox, QHBoxLayout, QSpacerItem, QSizePolicy, QCheckBox
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from client.main_elements import Customer, User, main_functions

class RegisterWindow(QWidget):
    def __init__(self, login_window):
        super().__init__()

        self.login_window = login_window

        self.setWindowTitle("Регистрация")
        self.setFixedSize(300, 250)
        self.setWindowIcon(QIcon('img/logo.png'))

        layout = QVBoxLayout()

        self.label_login = QLabel("Логин:", self)
        self.lineEdit_login = QLineEdit(self)

        self.label_password = QLabel("Пароль:", self)
        self.lineEdit_password = QLineEdit(self)
        self.lineEdit_password.setEchoMode(QLineEdit.EchoMode.Password)

        self.label_email = QLabel("Электронная почта:")
        self.lineEdit_email = QLineEdit(self)
        
        self.show_password_checkbox = QCheckBox("Показать пароль", self)
        self.show_password_checkbox.stateChanged.connect(self.toggle_password_visibility)

        layout.addWidget(self.label_login)
        layout.addWidget(self.lineEdit_login)
        layout.addWidget(self.label_password)
        layout.addWidget(self.lineEdit_password)
        layout.addWidget(self.label_email)
        layout.addWidget(self.lineEdit_email)
        layout.addWidget(self.show_password_checkbox)
        
        # Промежуток между виджетами
        layout.addSpacing(10)

        button_layout = QHBoxLayout()

        self.button_register = QPushButton("Зарегистрировать", self)
        self.button_register.clicked.connect(self.register_account)

        self.button_cancel = QPushButton("Отмена", self)
        self.button_cancel.clicked.connect(self.cancel_registration)

        # Промежуток между кнопками
        button_layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        button_layout.addWidget(self.button_register)
        button_layout.addWidget(self.button_cancel)
        button_layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))

        layout.addLayout(button_layout)

        self.setLayout(layout)

        # Отображение окна по центру экрана
        self.center()

    def toggle_password_visibility(self, state):
        if state == Qt.CheckState.Checked.value:
            self.lineEdit_password.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            self.lineEdit_password.setEchoMode(QLineEdit.EchoMode.Password)

    def register_account(self):
        user = User(login= self.lineEdit_login.text(), password= self.lineEdit_password.text())
        if len(user.login) > 5 and len(user.password) > 7:
            if main_functions.check_login_user(user) == None:
                if main_functions.check_email_customer(Customer(email = self.lineEdit_email.text())) == None:
                    if main_functions.register(user, Customer(email = self.lineEdit_email.text())) == 200:
                        QMessageBox.information(self, "Успех", "Аккаунт успешно зарегистрирован!")
                        self.close()
                        self.login_window.show()
                    else:
                        QMessageBox.information(self, "Провал", "Неудалось создать аккаунт.")
                else:
                    QMessageBox.information(self, "Провал", "Эта почта уже зарегистрирована.")
            else:
                QMessageBox.information(self, "Провал", "Этот логин занят.")
        else:
            QMessageBox.information(self, "Провал", "Логин должен состоять из 6 или более симоволов, а пароль из 8 и более!") 

        
    def cancel_registration(self):
        self.close()  
        self.login_window.show()

    def center(self):
        # Получаем размеры экрана
        screen = QApplication.primaryScreen().geometry()
        # Получаем размеры окна
        size = self.geometry()
        # Позиционируем окно по центру экрана
        self.move((screen.width() - size.width()) // 2, (screen.height() - size.height()) // 2)