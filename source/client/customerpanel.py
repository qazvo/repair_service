from PyQt6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox, QFormLayout, QDialog, QListWidget, QInputDialog, QApplication, QSizePolicy, QSpacerItem, QComboBox, QTextEdit, QCheckBox
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QIcon
from client.main_elements import Customer, main_functions, Appeal, Device, TypeDevice

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
        self.button_cancel.clicked.connect(self.close)

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
        customer = Customer(id = self.customer_id, FIO = self.lineEdit_fio.text(), address = self.lineEdit_address.text(), number_phone = self.lineEdit_phone.text())
        if not customer.FIO or not customer.address or not customer.number_phone:
            QMessageBox.warning(self, "Предупреждение", "Все поля должны быть заполнены")
            return
        result = main_functions.update_customer(customer)
        
        if result == 200:
            QMessageBox.information(self, "Успех", "Информация сохранена!")
            self.close()
            self.customer_window = CustomerWindow(self.customer_id)
            self.customer_window.show() 
        else:
            QMessageBox.critical(self, "Ошибка", "Неизвестная ошибка")

    def center(self):
        screen = QApplication.primaryScreen().geometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) // 2, (screen.height() - size.height()) // 2)

class CustomerWindow(QWidget):
    def __init__(self, customer_id):
        super().__init__()

        self.customer_id = customer_id

        self.setWindowTitle("Панель пользователя")
        self.setFixedSize(600, 400)
        self.setWindowIcon(QIcon('img/logo.png'))

        self.create_appeal_button = QPushButton("Создать обращение", self)
        self.create_appeal_button.clicked.connect(self.create_appeal)

        layout = QVBoxLayout()
        layout.addWidget(self.create_appeal_button)
        self.setLayout(layout)
        self.center()

    def create_appeal(self):
        self.edit_user_window = CreateAppealForm(self.customer_id, self)
        self.edit_user_window.show()

    def center(self):
        screen = QApplication.primaryScreen().geometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) // 2, (screen.height() - size.height()) // 2)

class CreateAppealForm(QDialog):
    def __init__(self, customer_id, parent=None):
        super().__init__(parent)

        self.customer_id = customer_id

        self.setWindowTitle("Создание нового обращения")
        self.setWindowIcon(QIcon('img/logo.png'))
        self.setFixedSize(375, 340)
        
        layout = QVBoxLayout()

        self.combobox_previous_devices = QComboBox()
        self.fill_previous_devices()

        self.label_previous_devices = QLabel("Ранее введеные устройства:")
        self.label_previous_devices.hide()
        layout.addWidget(self.label_previous_devices)

        layout.addWidget(self.combobox_previous_devices)
        self.combobox_previous_devices.hide()

        self.label_device_type = QLabel("Тип устройства:")
        self.comboBox_device_type = QComboBox()
        self.fill_device_types()

        layout.addWidget(self.label_device_type)
        layout.addWidget(self.comboBox_device_type)

        self.label_model = QLabel("Модель:")
        self.lineEdit_model = QLineEdit()

        self.label_serial_number = QLabel("Серийный номер:")
        self.lineEdit_serial_number = QLineEdit()

        layout.addWidget(self.label_model)
        layout.addWidget(self.lineEdit_model)
        layout.addWidget(self.label_serial_number)
        layout.addWidget(self.lineEdit_serial_number)

        self.label_description = QLabel("Описание проблемы:")
        self.textEdit_description = QTextEdit()

        layout.addWidget(self.label_description)
        layout.addWidget(self.textEdit_description)

        self.checkbox_select_previous = QCheckBox("Выбрать из ранее введенных устройств")
        self.checkbox_select_previous.stateChanged.connect(self.toggle_previous_device_fields)
        layout.addWidget(self.checkbox_select_previous)

        self.button_save = QPushButton("Создать")
        self.button_save.clicked.connect(self.save_appeal)

        self.button_cancel = QPushButton("Отмена")
        self.button_cancel.clicked.connect(self.close)

        layout.addWidget(self.button_save)
        layout.addWidget(self.button_cancel)

        self.setLayout(layout)

        self.center()

    def toggle_previous_device_fields(self, state):
        if state == Qt.CheckState.Checked.value:
            self.label_device_type.hide()
            self.comboBox_device_type.hide()
            self.label_model.hide()
            self.lineEdit_model.hide()
            self.label_serial_number.hide()
            self.lineEdit_serial_number.hide()
            self.combobox_previous_devices.show()
            self.label_previous_devices.show()
        else:
            self.label_device_type.show()
            self.comboBox_device_type.show()
            self.label_model.show()
            self.lineEdit_model.show()
            self.label_serial_number.show()
            self.lineEdit_serial_number.show()
            self.combobox_previous_devices.hide()
            self.label_previous_devices.hide()

    def fill_device_types(self):
        result = main_functions.load_types_devices()
        if result["code"] == 200 and result["data"]:
            types = [type[0] for type in result["data"]]
            self.comboBox_device_type.addItems(types)
        else:
            QMessageBox.critical(self, "Ошибка", "Не удалось загрузить типы устройств из базы данных.")
    def save_appeal(self):
        if self.checkbox_select_previous.isChecked():
            device = Device(id = main_functions.load_previous_device(Customer(id= self.customer_id), Device(model= self.combobox_previous_devices.currentText())))
            appeal = Appeal(customer_id= self.customer_id, description = self.textEdit_description.toPlainText())
            result = main_functions.add_appeal(appeal, device, previous_device= True)
            if result == 200:
                QMessageBox.information(self, "Успех", "Обращение создано!")
                self.close()
            else:
                QMessageBox.critical(self, "Ошибка", "Не удалось создать обращение.")
        else:
            device = Device(model = self.lineEdit_model.text(), serial_number = self.lineEdit_serial_number.text(), type_id= main_functions.type_device_definition(TypeDevice(name= self.comboBox_device_type.currentText())))
            appeal = Appeal(customer_id= self.customer_id ,description = self.textEdit_description.toPlainText())
            result = main_functions.add_appeal(appeal, device)
            if result == 200:
                QMessageBox.information(self, "Успех", "Обращение создано!")
                self.close()
            else:
                QMessageBox.critical(self, "Ошибка", "Не удалось создать обращение.")
    def fill_previous_devices(self):
        result = main_functions.load_previous_devices(Customer(id = self.customer_id))
        if result["code"] == 200:
            devices = [device[0] for device in result["data"]]
            self.combobox_previous_devices.addItems(devices)
        else:
            QMessageBox.critical(self, "Ошибка", "Не удалось загрузить типы устройств из базы данных.")

    def center(self):
        screen = QApplication.primaryScreen().geometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) // 2, (screen.height() - size.height()) // 2)
    