from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox, QSpacerItem, QSizePolicy, QFormLayout, QGroupBox, QMainWindow
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QIcon
from client.main_elements import Customer, main_functions

class InformationAboutCustomer(QWidget):
    def __init__(self, customer_id):
        super().__init__()

        self.customer_id = customer_id

        self.setWindowTitle("Добро пожаловать!")
        self.setFixedSize(400, 270)
        self.setWindowIcon(QIcon('img/logo.png'))

        self.welcome_label = QLabel("Добро пожаловать!", self)
        self.welcome_label.setWordWrap(True)
        self.welcome_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.welcome_label.setFont(QFont('Arial', 14))

        self.info_label = QLabel("Введите необходимые данные для продолжения работы", self)
        self.info_label.setWordWrap(True)
        self.info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.info_label.setFont(QFont('Arial', 12))


        form_layout = QFormLayout()
        form_layout.setSpacing(10)

        self.lineEdit_fio = QLineEdit(self)
        self.lineEdit_address = QLineEdit(self)
        self.lineEdit_phone = QLineEdit(self)

        form_layout.addRow(QLabel("ФИО"), self.lineEdit_fio)
        form_layout.addRow(QLabel("Адрес"), self.lineEdit_address)
        form_layout.addRow(QLabel("Номер телефона"), self.lineEdit_phone)

        self.button_save = QPushButton("Продолжить", self)
        self.button_cancel = QPushButton("Отмена", self)

        self.button_save.clicked.connect(self.save_client_info)
        self.button_cancel.clicked.connect(self.cancel)

        button_layout = QVBoxLayout()
        button_layout.addSpacing(10)
        button_layout.addWidget(self.button_save)
        button_layout.addWidget(self.button_cancel)
        main_layout = QVBoxLayout()

        main_layout.addSpacerItem(QSpacerItem(10, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))
        
        main_layout.addWidget(self.welcome_label)

        main_layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        main_layout.addWidget(self.info_label)
        
        main_layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))
        
        main_layout.addLayout(form_layout)
        main_layout.addStretch(1)
        main_layout.addLayout(button_layout)

        main_layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))
        
        self.setLayout(main_layout)
        self.center()

    def save_client_info(self):
        fio = self.lineEdit_fio.text()
        address = self.lineEdit_address.text()
        phone = self.lineEdit_phone.text()

        if not fio or not address or not phone:
            QMessageBox.warning(self, "Предупреждение", "Все поля должны быть заполнены")
            return
        result = main_functions.update_customer(Customer(FIO= fio, address= address, number_phone= phone, id = self.customer_id))
        
        if result == 200:
            QMessageBox.information(self, "Успех", "Информация сохранена!")
            self.close()
        else:
            QMessageBox.critical(self, "Ошибка", "Неизвестная ошибка")

    def cancel(self):
        self.close()

    def center(self):
        screen = QApplication.primaryScreen().geometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) // 2, (screen.height() - size.height()) // 2)

class CustomerWindow(QWidget):
    def __init__(self, customer_id):
        super().__init__()

        self.customer_id = customer_id

        self.setWindowTitle("Панель пользователя")
        self.setFixedSize(400, 270)