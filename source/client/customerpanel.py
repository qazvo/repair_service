from PyQt6.QtWidgets import QTableWidgetItem, QHeaderView, QTableView, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox, QFormLayout, QDialog, QListWidget, QInputDialog, QApplication, QSizePolicy, QSpacerItem, QComboBox, QTextEdit, QCheckBox, QStackedWidget, QTableWidget
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QStandardItemModel, QFont, QIcon, QPixmap
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
        self.setGeometry(100, 100, 1000, 600)
        self.setWindowIcon(QIcon('img/logo.png'))

        main_layout = QHBoxLayout()
        self.setLayout(main_layout)

        sidebar_widget = QWidget()
        sidebar_layout = QVBoxLayout()
        sidebar_widget.setLayout(sidebar_layout)

        logo_label = QLabel()
        pixmap = QPixmap("img/mastertechh.png")
        logo_label.setPixmap(pixmap)
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sidebar_layout.addWidget(logo_label)

        profile_button = QPushButton()
        profile_pixmap = QPixmap("img/profile.png") 
        profile_icon = QIcon(profile_pixmap)
        profile_button.setIcon(profile_icon)
        profile_button.setIconSize(profile_pixmap.size() / 2)
        profile_button.setFixedSize(profile_pixmap.size() / 2) 
        profile_button.setStyleSheet("QPushButton { background: transparent; border: none; }")  
        profile_button.clicked.connect(self.show_user_data)
        sidebar_layout.addWidget(profile_button, alignment=Qt.AlignmentFlag.AlignCenter)

        small_spacer = QSpacerItem(20, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sidebar_layout.addItem(small_spacer)

        requests_button = QPushButton("Мои обращения")
        requests_button.clicked.connect(self.show_appeals)
        sidebar_layout.addWidget(requests_button)

        approved_button = QPushButton("Одобренные заявки на ремонт")
        approved_button.clicked.connect(self.show_approved_applications)
        sidebar_layout.addWidget(approved_button)

        sidebar_layout.addStretch()

        main_layout.addWidget(sidebar_widget)

        self.content_widget = QStackedWidget()
        main_layout.addWidget(self.content_widget)

        self.appeals_table_widget = QWidget()
        self.appeals_table_layout = QVBoxLayout()
        self.appeals_table_widget.setLayout(self.appeals_table_layout)

        self.appeals_table = QTableWidget()
        self.appeals_table.setColumnCount(3)
        self.appeals_table.setHorizontalHeaderLabels(["Номер обращения", "Устройство", "Описание проблемы"])
        self.appeals_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.appeals_table.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)
        self.appeals_table.setSelectionMode(QTableView.SelectionMode.SingleSelection)
        self.appeals_table.setAlternatingRowColors(True)
        self.appeals_table.verticalHeader().setVisible(False)
        self.appeals_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        
        self.create_appeal_button = QPushButton("Создать обращение")
        self.create_appeal_button.clicked.connect(self.create_request)
        
        self.appeals_table_layout.addWidget(self.appeals_table)
        self.appeals_table_layout.addWidget(self.create_appeal_button)

        self.show_appeals()

        self.claims_table = QTableWidget()
        self.claims_table.setColumnCount(5)
        self.claims_table.setHorizontalHeaderLabels(["Номер заявки", "Дата приема", "Устройство", "Описание проблемы", "Статус"])
        self.claims_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.claims_table.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)
        self.claims_table.setSelectionMode(QTableView.SelectionMode.SingleSelection)
        self.claims_table.setAlternatingRowColors(True)
        self.claims_table.verticalHeader().setVisible(False)
        self.claims_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

        self.content_widget.addWidget(self.appeals_table_widget)
        self.content_widget.addWidget(self.claims_table)

        self.center()

    def show_user_data(self):
        user_data_widget = QWidget()
        user_data_layout = QVBoxLayout()
        user_data_widget.setLayout(user_data_layout)

        user_data_label = QLabel("Данные пользователя")
        user_data_label.setStyleSheet("font-size: 20px; font-weight: bold;")
        user_data_layout.addWidget(user_data_label, alignment=Qt.AlignmentFlag.AlignCenter)

        profile_data = main_functions.load_information_customer(Customer(id = self.customer_id))

        self.form_layout = QFormLayout()
        self.form_layout.setContentsMargins(50, 20, 50, 20)

        self.full_name_label = QLabel(profile_data[0])
        self.address_label = QLabel(profile_data[1])
        self.phone_label = QLabel(profile_data[2])
        self.email_label = QLabel(profile_data[3])

        labels = [self.full_name_label, self.address_label, self.phone_label, self.email_label]
        for label in labels:
            label.setStyleSheet("font-size: 16px; padding: 5px; border: 1px solid #ccc; border-radius: 5px;")
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.form_layout.addRow("ФИО:", self.full_name_label)
        self.form_layout.addRow("Адрес:", self.address_label)
        self.form_layout.addRow("Телефон:", self.phone_label)
        self.form_layout.addRow("Email:", self.email_label)

        user_data_layout.addLayout(self.form_layout)

        self.change_data_button = QPushButton("Изм. данные")
        self.change_data_button.setStyleSheet("padding: 10px; font-size: 16px;")
        self.change_data_button.clicked.connect(self.enable_editing)
        user_data_layout.addWidget(self.change_data_button, alignment=Qt.AlignmentFlag.AlignCenter)

        self.content_widget.addWidget(user_data_widget)
        self.content_widget.setCurrentWidget(user_data_widget)

    def enable_editing(self):
        self.full_name_input = QLineEdit(self.full_name_label.text())
        self.address_input = QLineEdit(self.address_label.text())
        self.phone_input = QLineEdit(self.phone_label.text())
        self.email_input = QLineEdit(self.email_label.text())

        inputs = [self.full_name_input, self.address_input, self.phone_input, self.email_input]
        for input_field in inputs:
            input_field.setStyleSheet("font-size: 16px; padding: 5px; border: 1px solid #ccc; border-radius: 5px;")

        self.form_layout.removeRow(self.full_name_label)
        self.form_layout.removeRow(self.address_label)
        self.form_layout.removeRow(self.phone_label)
        self.form_layout.removeRow(self.email_label)

        self.form_layout.insertRow(0, "ФИО:", self.full_name_input)
        self.form_layout.insertRow(1, "Адрес:", self.address_input)
        self.form_layout.insertRow(2, "Телефон:", self.phone_input)
        self.form_layout.insertRow(3, "Email:", self.email_input)

        save_button = QPushButton("Сохранить")
        save_button.setStyleSheet("padding: 10px; font-size: 16px;")
        save_button.clicked.connect(self.save_user_data)

        cancel_button = QPushButton("Отмена")
        cancel_button.setStyleSheet("padding: 10px; font-size: 16px;")
        cancel_button.clicked.connect(self.cancel_editing)

        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(save_button)
        buttons_layout.addWidget(cancel_button)

        self.form_layout.addRow(buttons_layout)

        self.change_data_button.setVisible(False)

    def cancel_editing(self):
        self.show_user_data()

    def save_user_data(self):
        customer = Customer(id = self.customer_id, FIO = self.full_name_input.text(), address=  self.address_input.text(), number_phone= self.phone_input.text(), email= self.email_input.text())
        main_functions.update_full_information_customer(customer)
        self.show_user_data()

    def show_appeals(self):
        appeals_data = main_functions.load_appeals(Customer(id = self.customer_id))
        self.appeals_table.setRowCount(len(appeals_data))
        for row, appeal in enumerate(appeals_data):
            for col, item in enumerate(appeal):
                self.appeals_table.setItem(row, col, QTableWidgetItem(str(item)))
        self.content_widget.setCurrentWidget(self.appeals_table_widget)

    def show_approved_applications(self):
        claims_data = main_functions.load_claims(Customer(id = self.customer_id))
        self.claims_table.setRowCount(len(claims_data))
        for row, claim in enumerate(claims_data):
            for col, item in enumerate(claim):
                self.claims_table.setItem(row, col, QTableWidgetItem(str(item)))
        self.content_widget.setCurrentWidget(self.claims_table)

    def create_request(self):
        self.create_appeal_form = CreateAppealForm(self.customer_id)
        self.create_appeal_form.show()

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
            device = Device(id = main_functions.definition_previous_device(Customer(id= self.customer_id), Device(model= self.combobox_previous_devices.currentText())))
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
    