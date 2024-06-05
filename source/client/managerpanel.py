from PyQt6.QtWidgets import (
    QTableWidget, QTableWidgetItem, QHeaderView, QTableView, QWidget,
    QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QTabWidget, QMessageBox, QApplication
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon

from client.main_elements import main_functions, Appeal

class ManagerWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Панель менеджера по заявкам")
        self.setFixedSize(1100, 700)
        self.setWindowIcon(QIcon('img/logo.png'))

        main_layout = QVBoxLayout(self)

        self.tab_widget = QTabWidget()
        main_layout.addWidget(self.tab_widget)

        self.appeals_data = None
        self.claims_data = None
        self.clients_data = None

        self.init_appeals_tab()
        self.init_claims_tab()
        self.init_clients_tab()

    def init_appeals_tab(self):
        self.appeals_tab = QWidget()
        self.appeals_layout = QVBoxLayout(self.appeals_tab)

        self.search_appeals_line_edit = QLineEdit()
        self.search_appeals_line_edit.setPlaceholderText("Поиск...")
        self.search_appeals_line_edit.textChanged.connect(self.search_appeals)

        self.appeals_table = QTableWidget()
        self.appeals_table.setColumnCount(4)
        self.appeals_table.setHorizontalHeaderLabels(["Номер обращения", "Клиент", "Устройство", "Описание проблемы"])
        self.appeals_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.appeals_table.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)
        self.appeals_table.setSelectionMode(QTableView.SelectionMode.SingleSelection)
        self.appeals_table.setAlternatingRowColors(True)
        self.appeals_table.verticalHeader().setVisible(False)
        self.appeals_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

        self.create_claim_button = QPushButton("Создать заявку")
        self.create_claim_button.setFixedHeight(30)
        self.create_claim_button.setMinimumWidth(100)
        self.create_claim_button.setIcon(QIcon("img/add.png"))
        self.create_claim_button.clicked.connect(self.create_claim_from_appeal)

        self.update_appeals_button = QPushButton()
        self.update_appeals_button.setFixedSize(28, 28)
        self.update_appeals_button.setIcon(QIcon('img/refresh.png'))
        self.update_appeals_button.clicked.connect(self.show_appeals)

        self.delete_appeal_button = QPushButton("Удалить обращение")
        self.delete_appeal_button.setFixedHeight(30)
        self.delete_appeal_button.setMinimumWidth(100)
        self.delete_appeal_button.setIcon(QIcon("img/delete.png"))
        self.delete_appeal_button.clicked.connect(self.delete_appeal)

        appeals_buttons_layout = QHBoxLayout()
        appeals_buttons_layout.addWidget(self.create_claim_button)
        appeals_buttons_layout.addWidget(self.delete_appeal_button)
        appeals_buttons_layout.addStretch()
        appeals_buttons_layout.addWidget(self.update_appeals_button)

        self.appeals_layout.addWidget(self.search_appeals_line_edit)
        self.appeals_layout.addWidget(self.appeals_table)
        self.appeals_layout.addLayout(appeals_buttons_layout)

        self.tab_widget.addTab(self.appeals_tab, "Обращения")

        self.show_appeals()

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

        claims_buttons_layout = QHBoxLayout()
        claims_buttons_layout.addStretch()
        claims_buttons_layout.addWidget(self.update_claims_button)

        self.claims_layout.addWidget(self.search_claims_line_edit)
        self.claims_layout.addWidget(self.claims_table)
        self.claims_layout.addLayout(claims_buttons_layout)

        self.tab_widget.addTab(self.claims_tab, "Заявки")

        self.show_claims()

    def init_clients_tab(self):
        self.clients_tab = QWidget()
        self.clients_layout = QVBoxLayout(self.clients_tab)

        self.search_clients_line_edit = QLineEdit()
        self.search_clients_line_edit.setPlaceholderText("Поиск...")
        self.search_clients_line_edit.textChanged.connect(self.search_clients)

        self.clients_table = QTableWidget()
        self.clients_table.setColumnCount(5)
        self.clients_table.setHorizontalHeaderLabels(["ID", "ФИО", "Адрес", "Телефон", "Email"])
        self.clients_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.clients_table.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)
        self.clients_table.setSelectionMode(QTableView.SelectionMode.SingleSelection)
        self.clients_table.setAlternatingRowColors(True)
        self.clients_table.verticalHeader().setVisible(False)
        self.clients_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

        self.update_clients_button = QPushButton()
        self.update_clients_button.setFixedSize(28, 28)
        self.update_clients_button.setIcon(QIcon('img/refresh.png'))
        self.update_clients_button.clicked.connect(self.show_claims)

        clients_buttons_layout = QHBoxLayout()
        clients_buttons_layout.addStretch()
        clients_buttons_layout.addWidget(self.update_clients_button)

        self.clients_layout.addWidget(self.search_clients_line_edit)
        self.clients_layout.addWidget(self.clients_table)
        self.clients_layout.addLayout(clients_buttons_layout)

        self.tab_widget.addTab(self.clients_tab, "Клиенты")

        self.show_clients()

        self.center()

    def show_appeals(self):
        self.appeals_data = main_functions.load_all_appeals()
        if self.appeals_data:
            self.display_appeals(self.appeals_data)

    def display_appeals(self, data):
        self.appeals_table.setRowCount(len(data))
        for row, appeal in enumerate(data):
            for col, item in enumerate(appeal):
                table_item = QTableWidgetItem("" if item is None else str(item))
                table_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.appeals_table.setItem(row, col, table_item)

    def show_claims(self):
        self.claims_data = main_functions.load_all_claims()
        if self.claims_data:
            self.display_claims(self.claims_data)
    
    def display_claims(self, data):
        self.claims_table.setRowCount(len(data))
        for row, claim in enumerate(data):
            for col, item in enumerate(claim):
                table_item = QTableWidgetItem("" if item is None else str(item))
                table_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.claims_table.setItem(row, col, table_item)

    def show_clients(self):
        self.clients_data = main_functions.load_all_customers()
        if self.clients_data:
            self.display_clients(self.clients_data)
    
    def display_clients(self, data):
        self.clients_table.setRowCount(len(data))
        for row, client in enumerate(data):
            for col, item in enumerate(client):
                table_item = QTableWidgetItem("" if item is None else str(item))
                table_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.clients_table.setItem(row, col, table_item)

    def search_appeals(self):
        query = self.search_appeals_line_edit.text().lower()
        filtered_data = [appeal for appeal in self.appeals_data if query in str(appeal).lower()]
        self.display_appeals(filtered_data)

    def search_claims(self):
        query = self.search_claims_line_edit.text().lower()
        filtered_data = [claim for claim in self.claims_data if query in str(claim).lower()]
        self.display_claims(filtered_data)

    def search_clients(self):
        query = self.search_clients_line_edit.text().lower()
        filtered_data = [client for client in self.clients_data if query in str(client).lower()]
        self.display_clients(filtered_data)

    def create_claim_from_appeal(self):
        selected_row = self.appeals_table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Предупреждение", "Пожалуйста, выберите обращение.")
            return
        appeal = Appeal(id = self.appeals_table.item(selected_row, 0).text())
        if main_functions.create_claim_from_appeal(appeal) == 200:
            QMessageBox.information(self, "Успех", "Заявка сформирована")
        else:
            QMessageBox.warning(self, "Провал", "Неудалось сформировать заявку")
        self.show_claims()
        self.show_appeals()
    
    def delete_appeal(self):
        selected_row = self.appeals_table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Предупреждение", "Пожалуйста, выберите обращение.")
            return
        appeal = Appeal(id = self.appeals_table.item(selected_row, 0).text())
        response = main_functions.delete_appeal(appeal)
        if response == 200:
            QMessageBox.information(self, "Успех", "Обращение удалено")
            self.show_appeals()
        else:
            QMessageBox.warning(self, "Ошибка", "Не удалось удалить обращение")

    def center(self):
        screen = QApplication.primaryScreen().geometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) // 2, (screen.height() - size.height()) // 2)
