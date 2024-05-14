from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QTableView, QPushButton, QHBoxLayout, QMessageBox,
    QGroupBox, QHeaderView, QSpacerItem, QSizePolicy, QDialog, QLabel, QLineEdit, QComboBox
)
from PyQt6.QtGui import QStandardItemModel, QStandardItem, QIcon
from PyQt6.QtCore import Qt
from client.main_elements import User, main_functions
from database.db_manager import db_manager

class CustomerWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Клиент")
        self.setFixedSize(300, 200)
        # Добавьте элементы и виджеты, необходимые для клиента

class MasterWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Мастер по ремонту")
        self.setFixedSize(300, 200)
        # Добавьте элементы и виджеты, необходимые для мастера

class ManagerWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Менеджер по заявкам")
        self.setFixedSize(300, 200)
        # Добавьте элементы и виджеты, необходимые для менеджера

class AdminWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Admin Panel")
        self.setFixedSize(800, 600)

        # Создаем виджет таблицы для отображения пользователей
        self.table_view = QTableView()
        self.table_model = QStandardItemModel()
        self.table_view.setModel(self.table_model)
        self.table_view.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table_view.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)
        self.table_view.setSelectionMode(QTableView.SelectionMode.SingleSelection)
        self.table_view.setAlternatingRowColors(True)
        self.table_view.setEditTriggers(QTableView.EditTrigger.NoEditTriggers)
        self.table_view.verticalHeader().setVisible(False)  # Скрываем номера строк

        # Загружаем данные пользователей из базы данных
        self.load_user_data()

        # Создаем кнопки для добавления, редактирования и удаления пользователей
        self.button_add_user = QPushButton("Add User")
        self.button_add_user.setIcon(QIcon("icons/add.png"))
        self.button_edit_user = QPushButton("Edit User")
        self.button_edit_user.setIcon(QIcon("icons/edit.png"))
        self.button_delete_user = QPushButton("Delete User")
        self.button_delete_user.setIcon(QIcon("icons/delete.png"))

        # Привязываем слоты к кнопкам
        self.button_add_user.clicked.connect(self.add_user)
        self.button_edit_user.clicked.connect(self.edit_user)
        self.button_delete_user.clicked.connect(self.delete_user)

        # Создаем компоновку для кнопок
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.button_add_user)
        button_layout.addWidget(self.button_edit_user)
        button_layout.addWidget(self.button_delete_user)

        # Промежуток между кнопками и таблицей
        button_layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))

        # Создаем групповой блок для управления пользователями
        group_box = QGroupBox("User Management")
        group_box_layout = QVBoxLayout()
        group_box_layout.addWidget(self.table_view)
        group_box_layout.addLayout(button_layout)
        group_box.setLayout(group_box_layout)

        # Главная компоновка
        main_layout = QVBoxLayout()
        main_layout.addWidget(group_box)
        self.setLayout(main_layout)

        # Центрируем окно на экране
        self.center()

    def load_user_data(self):
        # Запрос к базе данных для получения всех пользователей
        query = "SELECT id, login, password, type_id FROM users"
        result = db_manager.execute(query, many=True)

        # Проверяем результат
        if result["code"] == 200 and result["data"]:
            # Устанавливаем заголовки колонок
            self.table_model.setHorizontalHeaderLabels(["ID", "Login", "Password", "Role"])

            # Очищаем текущие данные модели
            self.table_model.removeRows(0, self.table_model.rowCount())

            # Заполняем модель данными
            for user_data in result["data"]:
                row = [QStandardItem(str(data)) for data in user_data]
                self.table_model.appendRow(row)
        else:
            QMessageBox.critical(self, "Error", "Failed to load user data.")

    def add_user(self):
        self.add_user_window = AddUserWindow(self)
        self.add_user_window.show()

    def edit_user(self):
        # Получаем выбранную строку
        selected_row = self.table_view.selectionModel().currentIndex().row()

        if selected_row >= 0:
            # Получаем данные пользователя из выбранной строки
            user_id = self.table_model.item(selected_row, 0).text()
            login = self.table_model.item(selected_row, 1).text()
            password = self.table_model.item(selected_row, 2).text()
            role = self.table_model.item(selected_row, 3).text()

            # Открываем окно редактирования пользователя
            self.edit_user_window = EditUserWindow(user_id, login, password, role, self)
            self.edit_user_window.show()
        else:
            QMessageBox.warning(self, "Warning", "Please select a user to edit.")

    def delete_user(self):
        # Получаем выбранную строку
        selected_row = self.table_view.selectionModel().currentIndex().row()

        if selected_row >= 0:
            # Получаем идентификатор пользователя из выбранной строки
            user_id = self.table_model.item(selected_row, 0).text()

            # Показываем диалоговое окно подтверждения удаления
            confirmation = QMessageBox.question(self, "Delete User", 
                                                 "Are you sure you want to delete this user?",
                                                 QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if confirmation == QMessageBox.StandardButton.Yes:
                # Удаляем пользователя из базы данных
                query = "DELETE FROM users WHERE id = ?"
                result = db_manager.execute(query, args=(user_id,))

                if result["code"] == 200:
                    # Обновляем модель данных
                    self.load_user_data()
                    QMessageBox.information(self, "Success", "User successfully deleted.")
                else:
                    QMessageBox.critical(self, "Error", "Failed to delete user.")
        else:
            QMessageBox.warning(self, "Warning", "Please select a user to delete.")

    def center(self):
        # Получаем размеры экрана
        screen = QApplication.primaryScreen().geometry()
        # Получаем размеры окна
        size = self.geometry()
        # Позиционируем окно по центру экрана
        self.move((screen.width() - size.width()) // 2, (screen.height() - size.height()) // 2)

class EditUserWindow(QDialog):
    def __init__(self, user_id, login, password, role, parent=None):
        super().__init__(parent)

        self.user_id = user_id
        self.setWindowTitle("Edit User")
        self.setFixedSize(300, 200)

        layout = QVBoxLayout(self)

        self.label_login = QLabel("Login:")
        self.lineEdit_login = QLineEdit(login)

        self.label_password = QLabel("Password:")
        self.lineEdit_password = QLineEdit(password)

        self.label_role = QLabel("Role:")
        self.comboBox_role = QComboBox()
        self.load_roles()
        self.comboBox_role.setCurrentText(role)

        layout.addWidget(self.label_login)
        layout.addWidget(self.lineEdit_login)
        layout.addWidget(self.label_password)
        layout.addWidget(self.lineEdit_password)
        layout.addWidget(self.label_role)
        layout.addWidget(self.comboBox_role)

        button_layout = QHBoxLayout()
        self.button_save = QPushButton("Save")
        self.button_cancel = QPushButton("Cancel")

        button_layout.addWidget(self.button_save)
        button_layout.addWidget(self.button_cancel)

        layout.addLayout(button_layout)

        self.button_save.clicked.connect(self.save_user)
        self.button_cancel.clicked.connect(self.close)

        # Центрируем окно на экране
        self.center()

    def load_roles(self):
        query = "SELECT name FROM types_users"
        result = db_manager.execute(query, many=True)
        if result["code"] == 200 and result["data"]:
            roles = [role[0] for role in result["data"]]
            self.comboBox_role.addItems(roles)
        else:
            QMessageBox.critical(self, "Error", "Failed to load roles from the database.")

    def save_user(self):
        login = self.lineEdit_login.text()
        password = self.lineEdit_password.text()
        role = self.comboBox_role.currentText()

        if not login or not password:
            QMessageBox.warning(self, "Warning", "Login and password cannot be empty.")
            return

        if len(login) < 6 or len(password) < 6:
            QMessageBox.warning(self, "Warning", "Login and password must be at least 6 characters long.")
            return
        
        # Определяем роль в виде числового значения
        role_query = "SELECT id FROM types_users WHERE name = ?"
        role_result = db_manager.execute(role_query, args=(role,))
        role_id = role_result["data"][0]

        # Обновляем данные пользователя в базе данных
        query = "UPDATE users SET login = ?, password = ?, type_id = ? WHERE id = ?"
        result = db_manager.execute(query, args=(login, password, role_id, self.user_id))

        if result["code"] == 200:
            self.parent().load_user_data()
            QMessageBox.information(self, "Success", "User information updated successfully.")
            self.close()
        else:
            QMessageBox.critical(self, "Error", "Failed to update user information.")

    def center(self):
        # Получаем размеры экрана
        screen = QApplication.primaryScreen().geometry()
        # Получаем размеры окна
        size = self.geometry()
        # Позиционируем окно по центру экрана
        self.move((screen.width() - size.width()) // 2, (screen.height() - size.height()) // 2)

class AddUserWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Add User")
        self.setFixedSize(300, 200)

        layout = QVBoxLayout(self)

        self.label_login = QLabel("Login:")
        self.lineEdit_login = QLineEdit()

        self.label_password = QLabel("Password:")
        self.lineEdit_password = QLineEdit()

        self.label_role = QLabel("Role:")
        self.comboBox_role = QComboBox()
        self.load_roles()

        layout.addWidget(self.label_login)
        layout.addWidget(self.lineEdit_login)
        layout.addWidget(self.label_password)
        layout.addWidget(self.lineEdit_password)
        layout.addWidget(self.label_role)
        layout.addWidget(self.comboBox_role)

        button_layout = QHBoxLayout()
        self.button_save = QPushButton("Save")
        self.button_cancel = QPushButton("Cancel")

        button_layout.addWidget(self.button_save)
        button_layout.addWidget(self.button_cancel)

        layout.addLayout(button_layout)

        self.button_save.clicked.connect(self.save_user)
        self.button_cancel.clicked.connect(self.close)

        # Центрируем окно на экране
        self.center()

    def load_roles(self):
        query = "SELECT name FROM types_users"
        result = db_manager.execute(query, many=True)
        if result["code"] == 200 and result["data"]:
            roles = [role[0] for role in result["data"]]
            self.comboBox_role.addItems(roles)
        else:
            QMessageBox.critical(self, "Error", "Failed to load roles from the database.")

    def save_user(self):
        login = self.lineEdit_login.text()
        password = self.lineEdit_password.text()
        role = self.comboBox_role.currentText()
        
        # Проверка на пустые поля и минимальную длину
        if not login or not password:
            QMessageBox.warning(self, "Warning", "Login and password cannot be empty.")
            return

        if len(login) < 6 or len(password) < 6:
            QMessageBox.warning(self, "Warning", "Login and password must be at least 6 characters long.")
            return

        # Определяем роль в виде числового значения
        role_query = "SELECT id FROM types_users WHERE name = ?"
        role_result = db_manager.execute(role_query, args=(role,))
        if role_result["data"] is not None:
            role_id = role_result["data"][0]

            # Добавляем нового пользователя в базу данных
            query = "INSERT INTO users (login, password, type_id) VALUES (?, ?, ?)"
            result = db_manager.execute(query, args=(login, password, role_id))

            if result["code"] == 200:
                self.parent().load_user_data()
                QMessageBox.information(self, "Success", "New user added successfully.")
                self.close()
            else:
                QMessageBox.critical(self, "Error", "Failed to add new user.")
        else:
            QMessageBox.critical(self, "Error", "Invalid role selected.")

    def center(self):
        # Получаем размеры экрана
        screen = QApplication.primaryScreen().geometry()
        # Получаем размеры окна
        size = self.geometry()
        # Позиционируем окно по центру экрана
        self.move((screen.width() - size.width()) // 2, (screen.height() - size.height()) // 2)