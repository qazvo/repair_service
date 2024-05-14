from database.db_manager import db_manager
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox, QHBoxLayout, QSpacerItem, QSizePolicy

class User:
    def __init__(self, id: int = None, login: str = None,  password: str = None, type_id: int = None):
        self.id = id
        self.login = login
        self.password = password
        self.type_id = type_id
    def to_json(self):
        return f'{{"id": "{self.id}""login": "{self.login}", "password": "{self.password}", "type_id": {self.type_id}}}'
class Customer:
    def __init__(self, id: int = None, FIO: str = None,  adress: str = None, number_phone: int = None, email: int = None):
        self.id = id
        self.FIO = FIO
        self.adress = adress
        self.number_phone = number_phone
        self.email = email
    def to_json(self):
        return f'{{"id": "{self.id}""FIO": "{self.FIO}", "adress": "{self.adress}", "number_phone": {self.number_phone}, "email": {self.email}}}'

class MainFunctions:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def login(self, user: User) -> tuple:
        result = db_manager.execute("""SELECT * FROM users WHERE login = ? AND password = ?""", args=(user.login, user.password))
        if result["data"]:
            return User(id = result["data"][0], type_id = result["data"][3])
        
    def check_login_user(self, user: User) -> tuple:
        result = db_manager.execute("""SELECT id FROM users WHERE login = ?""", args= (user.login,))
        if result["data"]:
            return result["data"][0]
        
    def check_email_customer(self, customer: Customer) -> tuple:
        result = db_manager.execute("""SELECT id FROM customers WHERE email = ?""", args= (customer.email,))
        if result["data"]:
            return result["data"][0]

    def register(self, user: User, customer: Customer) -> tuple:
        result = db_manager.execute("""INSERT INTO users (login, password, type_id) VALUES (?, ?, 4)""", args = (user.login, user.password))
        for_user_id = db_manager.execute("""SELECT id FROM users WHERE login == ?""", args = (user.login,))
        db_manager.execute("""INSERT INTO customers (email, user_id) VALUES (?, ?)""", args = (customer.email, for_user_id["data"][0]))
        return result["code"]
    
main_functions = MainFunctions(db_manager)