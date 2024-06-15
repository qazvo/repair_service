from PyQt6.QtWidgets import (
    QApplication, QTableWidget, QTableWidgetItem, QHeaderView, QTableView, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QTabWidget, QMessageBox, QLineEdit, QComboBox, QLabel, QDialog, QFormLayout
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon

from client.main_elements import main_functions, Employee, Contract, Status, Claim, Tool, ToolUsed

class MasterWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Панель мастера")
        self.setFixedSize(1200, 800)
        self.setWindowIcon(QIcon('img/logo.png'))

        main_layout = QVBoxLayout(self)

        self.tab_widget = QTabWidget()
        main_layout.addWidget(self.tab_widget)

        self.init_claims_tab()
        self.init_contracts_tab()

        self.setLayout(main_layout)

    def init_claims_tab(self):
        self.claims_tab = QWidget()
        self.claims_layout = QVBoxLayout(self.claims_tab)

        self.search_claims_line_edit = QLineEdit()
        self.search_claims_line_edit.setPlaceholderText("Поиск...")
        self.search_claims_line_edit.textChanged.connect(self.search_claims)

        self.claims_table = QTableWidget()
        self.claims_table.setColumnCount(7)
        self.claims_table.setHorizontalHeaderLabels(["Номер заявки", "Клиент", "Устройство", "Описание проблемы", "Дата приема", "Дата выполнения", "Статус"])
        self.claims_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.claims_table.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)
        self.claims_table.setSelectionMode(QTableView.SelectionMode.SingleSelection)
        self.claims_table.setAlternatingRowColors(True)
        self.claims_table.verticalHeader().setVisible(False)
        self.claims_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

        self.update_claims_button = QPushButton()
        self.update_claims_button.setFixedSize(28, 28)
        self.update_claims_button.setIcon(QIcon('img/refresh.png'))
        self.update_claims_button.clicked.connect(self.show_claims)

        self.status_label = QLabel("Обновить статус:")
        self.status_combobox = QComboBox()

        status = main_functions.load_statuses()
        statuses = [st[0] for st in status]
        self.status_combobox.addItems(statuses)

        self.update_status_button = QPushButton("Обновить статус")
        self.update_status_button.clicked.connect(self.update_claim_status)
        self.update_status_button.setIcon(QIcon("img/edit.png"))

        self.create_contract_button = QPushButton("Создать контракт")
        self.create_contract_button.clicked.connect(self.open_create_contract_dialog)
        self.create_contract_button.setIcon(QIcon("img/add.png"))

        self.filter_status_combobox = QComboBox()
        self.filter_status_combobox.addItem("Все")
        self.filter_status_combobox.addItems(statuses)
        self.filter_status_combobox.currentIndexChanged.connect(self.filter_claims_by_status)

        claims_buttons_layout = QHBoxLayout()
        claims_buttons_layout.addWidget(self.search_claims_line_edit)
        claims_buttons_layout.addWidget(self.filter_status_combobox)

        status_update_layout = QHBoxLayout()
        status_update_layout.addWidget(self.create_contract_button)
        status_update_layout.addWidget(self.update_status_button)
        status_update_layout.addWidget(self.status_label)
        status_update_layout.addWidget(self.status_combobox)
        status_update_layout.addStretch(1)
        status_update_layout.addWidget(self.update_claims_button)

        self.claims_layout.addLayout(claims_buttons_layout)
        self.claims_layout.addWidget(self.claims_table)
        self.claims_layout.addLayout(status_update_layout)

        self.tab_widget.addTab(self.claims_tab, "Заявки")

        self.show_claims()

    def init_contracts_tab(self):
        self.contracts_tab = QWidget()
        self.contracts_layout = QVBoxLayout(self.contracts_tab)

        self.search_contracts_line_edit = QLineEdit()
        self.search_contracts_line_edit.setPlaceholderText("Поиск...")
        self.search_contracts_line_edit.textChanged.connect(self.search_contracts)

        self.contracts_table = QTableWidget()
        self.contracts_table.setColumnCount(6)
        self.contracts_table.setHorizontalHeaderLabels(["Номер контракта", "Сотрудник", "Номер заявки", "Описание", "Стоимость", "Инструменты"])
        self.contracts_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.contracts_table.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)
        self.contracts_table.setSelectionMode(QTableView.SelectionMode.SingleSelection)
        self.contracts_table.setAlternatingRowColors(True)
        self.contracts_table.verticalHeader().setVisible(False)
        self.contracts_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

        self.update_contracts_button = QPushButton()
        self.update_contracts_button.setFixedSize(28, 28)
        self.update_contracts_button.setIcon(QIcon('img/refresh.png'))
        self.update_contracts_button.clicked.connect(self.show_contracts)

        self.edit_description_button = QPushButton("Изменить описание")
        self.edit_description_button.clicked.connect(self.edit_contract_description)
        self.edit_description_button.setIcon(QIcon("img/edit.png"))

        self.attach_tool_button = QPushButton("Прикрепить инструмент")
        self.attach_tool_button.clicked.connect(self.attach_tool_to_contract)
        self.attach_tool_button.setIcon(QIcon("img/add.png"))

        contracts_buttons_layout = QHBoxLayout()
        contracts_buttons_layout.addWidget(self.attach_tool_button)
        contracts_buttons_layout.addWidget(self.edit_description_button)
        contracts_buttons_layout.addStretch(1)
        contracts_buttons_layout.addWidget(self.update_contracts_button)

        self.contracts_layout.addWidget(self.search_contracts_line_edit)
        self.contracts_layout.addWidget(self.contracts_table)
        self.contracts_layout.addLayout(contracts_buttons_layout)

        self.tab_widget.addTab(self.contracts_tab, "Контракты")

        self.show_contracts()

    def show_claims(self):
        self.claims_data = main_functions.load_all_claims()
        if self.claims_data:
            self.display_claims(self.claims_data)

    def show_contracts(self):
        self.contracts_data = main_functions.load_all_contracts()
        if self.contracts_data:
            self.display_contracts(self.contracts_data)

    def display_claims(self, data):
        self.claims_table.setRowCount(len(data))
        for row, claim in enumerate(data):
            for col, item in enumerate(claim):
                table_item = QTableWidgetItem("" if item is None else str(item))
                table_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.claims_table.setItem(row, col, table_item)

    def display_contracts(self, data):
        self.contracts_table.setRowCount(len(data))
        for row, contract in enumerate(data):
            for col, item in enumerate(contract):
                table_item = QTableWidgetItem("" if item is None else str(item))
                table_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.contracts_table.setItem(row, col, table_item)

    def update_claim_status(self):
        selected_row = self.claims_table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Предупреждение", "Пожалуйста, выберите заявку.")
            return
        claim_id = self.claims_table.item(selected_row, 0).text()
        status_name = self.status_combobox.currentText()
        status_id = main_functions.status_definition(Status(name=status_name))
        response = main_functions.update_status_in_claim(Claim(id=claim_id, status_id=status_id))
        if response == 200:
            QMessageBox.information(self, "Успех", "Статус заявки обновлен")
            self.show_claims()
        else:
            QMessageBox.warning(self, "Ошибка", "Не удалось обновить статус заявки")

    def open_create_contract_dialog(self):
        selected_row = self.claims_table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Предупреждение", "Пожалуйста, выберите заявку.")
            return

        claim_id = self.claims_table.item(selected_row, 0).text()
        dialog = CreateContractDialog(self, claim_id)
        dialog.exec()

    def edit_contract_description(self):
        selected_row = self.contracts_table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Предупреждение", "Пожалуйста, выберите контракт.")
            return

        contract_id = self.contracts_table.item(selected_row, 0).text()

        description_dialog = EditDescriptionDialog(self, contract_id)
        description_dialog.exec()

    def attach_tool_to_contract(self):
        selected_row = self.contracts_table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Предупреждение", "Пожалуйста, выберите контракт.")
            return

        contract_id = self.contracts_table.item(selected_row, 0).text()

        tool_dialog = AttachToolDialog(self, contract_id)
        tool_dialog.exec()

    def filter_claims_by_status(self):
        selected_status = self.filter_status_combobox.currentText()
        if selected_status == "Все":
            self.display_claims(self.claims_data, self.claims_table)
        else:
            filtered_data = [claim for claim in self.claims_data if claim[6] == selected_status]
            self.display_claims(filtered_data, self.claims_table)

    def search_claims(self):
        query = self.search_claims_line_edit.text().lower()
        filtered_data = [claim for claim in self.claims_data if query in str(claim).lower()]
        self.display_claims(filtered_data, self.claims_table)

    def search_contracts(self):
        query = self.search_contracts_line_edit.text().lower()
        filtered_data = [contract for contract in self.contracts_data if query in str(contract).lower()]
        self.display_contracts(filtered_data)

class CreateContractDialog(QDialog):
    def __init__(self, parent, claim_id):
        super().__init__(parent)
        self.claim_id = claim_id

        self.setFixedSize(400, 100)

        self.setWindowTitle("Создание контракта")
        self.layout = QVBoxLayout(self)

        form_layout = QFormLayout()
        self.employee_combobox = QComboBox()
        employees = main_functions.load_all_masters()
        employee_names = [emp[0] for emp in employees]
        self.employee_combobox.addItems(employee_names)

        self.cost_line_edit = QLineEdit()
        form_layout.addRow("Сотрудник:", self.employee_combobox)
        form_layout.addRow("Стоимость:", self.cost_line_edit)
        self.layout.addLayout(form_layout)

        button_layout = QHBoxLayout()
        self.save_button = QPushButton("Сохранить")
        self.save_button.clicked.connect(self.save_contract)
        button_layout.addWidget(self.save_button)
        self.layout.addLayout(button_layout)

    def save_contract(self):
        employee_name = self.employee_combobox.currentText()
        cost = self.cost_line_edit.text()
        employee_id = main_functions.employee_definition(Employee(FIO=employee_name))
        contract = Contract(claim_id=self.claim_id, employee_id=employee_id, cost=cost)
        response = main_functions.create_contract(contract)
        if response == 200:
            QMessageBox.information(self, "Успех", "Контракт создан")
            self.accept()
            self.parent().show_contracts()
        else:
            QMessageBox.warning(self, "Ошибка", "Не удалось создать контракт")
            self.reject()

class EditDescriptionDialog(QDialog):
    def __init__(self, parent, contract_id):
        super().__init__(parent)
        self.contract_id = contract_id

        self.setFixedSize(400, 80)

        self.setWindowTitle("Изменение описания")
        self.layout = QVBoxLayout(self)

        form_layout = QFormLayout()
        self.description_edit = QLineEdit()
        form_layout.addRow("Описание:", self.description_edit)
        self.layout.addLayout(form_layout)

        button_layout = QHBoxLayout()
        self.save_button = QPushButton("Сохранить")
        self.save_button.clicked.connect(self.save_description)
        button_layout.addWidget(self.save_button)
        self.layout.addLayout(button_layout)

    def save_description(self):
        description = self.description_edit.text()
        contract = Contract(id=self.contract_id, description_work_done=description)
        response = main_functions.update_description_in_contract(contract)
        if response == 200:
            QMessageBox.information(self, "Успех", "Описание изменено")
            self.accept()
            self.parent().show_contracts()
        else:
            QMessageBox.warning(self, "Ошибка", "Не удалось изменить описание")
            self.reject()

class AttachToolDialog(QDialog):
    def __init__(self, parent, contract_id):
        super().__init__(parent)
        self.contract_id = contract_id

        self.setFixedSize(400, 80)

        self.setWindowTitle("Прикрепление компонента")
        self.layout = QVBoxLayout(self)

        form_layout = QFormLayout()
        self.component_combobox = QComboBox()
        component = main_functions.load_components()
        components = [tl[0] for tl in component]
        self.component_combobox.addItems(components)

        form_layout.addRow("Компоненты:", self.component_combobox)
        self.layout.addLayout(form_layout)

        button_layout = QHBoxLayout()
        self.save_button = QPushButton("Сохранить")
        self.save_button.clicked.connect(self.save_component)
        button_layout.addWidget(self.save_button)
        self.layout.addLayout(button_layout)

    def save_component(self):
        component_name = self.component_combobox.currentText()
        component_id = main_functions.tool_definition(Tool(name=component_name))
        componentused = ToolUsed(contract_id=self.contract_id, tool_id=component_id)
        response = main_functions.add_component(componentused)
        if response == 200:
            QMessageBox.information(self, "Успех", "Компонент прикреплен")
            self.accept()
            self.parent().show_contracts()
        else:
            QMessageBox.warning(self, "Ошибка", "Не удалось прикрепить компонент")
            self.reject()