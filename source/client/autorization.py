from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox, QHBoxLayout, QSpacerItem, QSizePolicy
from PyQt6.QtGui import QIcon
from client.main_elements import User, main_functions, Customer
from client.registration import RegisterWindow
from client.adminpanel import AdminWindow
from client.masterpanel import MasterWindow, ManagerWindow
from client.customerpanel import InformationAboutCustomer, CustomerWindow

class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Авторизация")
        self.setFixedSize(300, 150)
        self.setWindowIcon(QIcon('img/logo.png'))

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
        user = main_functions.login(User(login=self.lineEdit_username.text(), password=self.lineEdit_password.text()))
        if user:
            if user.type_id == 4:
                # Клиент
                customer_id = main_functions.client_definition(User(id = user.id))
                if main_functions.is_user_already_registered(Customer(id = customer_id)):
                    self.customer_window = CustomerWindow(customer_id)
                    self.customer_window.show()  
                else: 
                    self.information_about_customer = InformationAboutCustomer(customer_id)
                    self.information_about_customer.show() 
            elif user.type_id == 3:
                # Менеджер по заявкам
                self.manager_window = ManagerWindow()
                self.manager_window.show()
            elif user.type_id == 2:
                # Мастер по ремонту
                self.master_window = MasterWindow()
                self.master_window.show()
            elif user.type_id == 1:
                # Администратор
                self.admin_window = AdminWindow()
                self.admin_window.show()
            self.close()
        else:
            QMessageBox.information(self, "Провал", "Неверный логин или пароль!")


    def open_register_window(self):
        self.hide()
        self.register_window = RegisterWindow(self)
        self.register_window.show()

    def center(self):
        # Получаем размеры экрана
        screen = QApplication.primaryScreen().geometry()
        # Получаем размеры окна
        size = self.geometry()
        # Позиционируем окно по центру экрана
        self.move((screen.width() - size.width()) // 2, (screen.height() - size.height()) // 2)