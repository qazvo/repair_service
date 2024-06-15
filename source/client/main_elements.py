from database.db_manager import db_manager

class User:
    def __init__(self, id: int = None, login: str = None,  password: str = None, type_id: int = None):
        self.id = id
        self.login = login
        self.password = password
        self.type_id = type_id
    
class Device:
    def __init__(self, id: int = None, type_id: int = None,  model: str = None, serial_number: str = None):
        self.id = id
        self.type_id = type_id
        self.model = model
        self.serial_number = serial_number
    
class Appeal:
    def __init__(self, id: int = None, customer_id: int = None,  device_id: int = None, description: str = None):
        self.id = id
        self.customer_id = customer_id
        self.device_id = device_id
        self.description = description
    
class Customer:
    def __init__(self, id: int = None, FIO: str = None,  address: str = None, number_phone: str = None, email: str = None):
        self.id = id
        self.FIO = FIO
        self.address = address
        self.number_phone = number_phone
        self.email = email
    
class TypeUser:
    def __init__(self, id: int = None, name: str = None):
        self.id = id
        self.name = name
    
class TypeDevice:
    def __init__(self, id: int = None, name: str = None):
        self.id = id
        self.name = name

class Claim:
    def __init__(self, id: int = None, appeal_id: int = None,  start_date: str = None, end_date: str = None, status_id: int = None):
        self.id = id
        self.appeal_id = appeal_id
        self.start_date = start_date
        self.end_date = end_date
        self.status_id = status_id

class Contract:
    def __init__(self, id: int = None, employee_id: int = None, claim_id: int = None, description_work_done: str = None, cost: float = None):
        self.id = id
        self.employee_id = employee_id
        self.claim_id = claim_id
        self.description_work_done = description_work_done
        self.cost = cost

class Employee:
    def __init__(self, id: int = None, FIO: str = None, post_id: int = None):
        self.id = id
        self.FIO = FIO
        self.post_id = post_id

class Status:
    def __init__(self, id: int = None, name: str = None):
        self.id = id
        self.name = name

class Tool:
    def __init__(self, id: int = None, name: str = None):
        self.id = id
        self.name = name

class ToolUsed:
    def __init__(self, contract_id: int = None, tool_id: int = None):
        self.contract_id = contract_id
        self.tool_id = tool_id

class MainFunctions:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def login(self, user: User) -> tuple:
        result = db_manager.execute("""SELECT id, type_id FROM users WHERE login = ? AND password = ?""", args=(user.login, user.password))
        if result["data"]:
            return User(id = result["data"][0], type_id = result["data"][1])
        
    def check_login_user(self, user: User) -> tuple:
        result = db_manager.execute("""SELECT id FROM users WHERE login = ?""", args= (user.login,))
        if result["data"]:
            return result["data"][0]
        
    def check_email_customer(self, customer: Customer) -> tuple:
        result = db_manager.execute("""SELECT id FROM customers WHERE email = ?""", args= (customer.email,))
        if result["data"]:
            return result["data"][0]

    def register(self, user: User, customer: Customer):
        result = db_manager.execute("""INSERT INTO users (login, password, type_id) VALUES (?, ?, 4)""", args = (user.login, user.password))
        for_user_id = db_manager.execute("""SELECT id FROM users WHERE login == ?""", args = (user.login,))
        db_manager.execute("""INSERT INTO customers (email, user_id) VALUES (?, ?)""", args = (customer.email, for_user_id["data"][0]))
        return result["code"]
    
    def load_user_data(self) -> tuple:
        result = db_manager.execute("""SELECT users.id, users.login, users.password, types_users.name FROM users JOIN types_users ON users.type_id = types_users.id""", many=True)
        return result
    
    def delete_user(self, user: User):
        result = db_manager.execute("""DELETE FROM users WHERE id = ?""", args= (user.id,))
        return result["code"]
    
    def load_roles(self) -> tuple:
        result = db_manager.execute("""SELECT name FROM types_users""", many= True)
        return result
    
    def role_definition(self, typeuser: TypeUser) -> int:
        result = db_manager.execute("""SELECT id FROM types_users WHERE name = ?""", args= (typeuser.name,))
        return result["data"][0]
    
    def update_user(self, user: User):
        result = db_manager.execute("""UPDATE users SET login = ?, password = ?, type_id = ? WHERE id = ?""", args= (user.login, user.password, user.type_id, user.id))
        return result["code"]
    
    def add_user(self, user: User):
        result = db_manager.execute("""INSERT INTO users (login, password, type_id) VALUES (?, ?, ?)""", args= (user.login, user.password, user.type_id))
        return result["code"]
    
    def client_definition(self, user: User):
        result = db_manager.execute("""SELECT id FROM customers WHERE user_id = ?""", args= (user.id,))
        return result["data"][0]
    
    def is_user_already_registered(self, customer:  Customer):
        result = db_manager.execute("""SELECT FIO, address, number_phone FROM customers WHERE id = ?""", args= (customer.id,))
        fio, address, phone = result["data"]
        if fio and address and phone:
            return True
        return False
    
    def update_customer(self, customer: Customer):
        result = db_manager.execute("""UPDATE customers SET FIO = ?, address = ?, number_phone = ? WHERE id = ?""", args= (customer.FIO, customer.address, customer.number_phone, customer.id))
        return result["code"]
    
    def load_types_devices(self) -> tuple:
        result = db_manager.execute("""SELECT name FROM types_devices""", many= True)
        return result
    
    def load_previous_devices(self, customer: Customer) -> tuple:
        result = db_manager.execute("""SELECT DISTINCT d.model
                                        FROM appeals a
                                        JOIN devices d ON a.device_id = d.id
                                        JOIN types_devices td ON d.type_id = td.id
                                        WHERE a.customer_id = ?""", args= (customer.id,), many= True)
        return result
    
    def type_device_definition(self, typedevice: TypeDevice) -> int:
        result = db_manager.execute("""SELECT id FROM types_devices WHERE name = ?""", args= (typedevice.name,))
        return result["data"][0]
    
    def add_appeal(self, appeal: Appeal, device: Device, previous_device: bool = None):
        if previous_device:
            result_appeal = db_manager.execute("""INSERT INTO appeals(customer_id, device_id, description) VALUES (?, ?, ?)""", args= (appeal.customer_id, device.id, appeal.description))
            return result_appeal["code"]
        else:
            db_manager.execute("""INSERT INTO devices (type_id, model, serial_number) VALUES (?, ?, ?)""", args= (device.type_id, device.model, device.serial_number))
            for_device_id = db_manager.execute("""SELECT id FROM devices WHERE model == ? AND serial_number == ?""", args = (device.model, device.serial_number))
            result_appeal = db_manager.execute("""INSERT INTO appeals(customer_id, device_id, description) VALUES (?, ?, ?)""", args= (appeal.customer_id, for_device_id["data"][0], appeal.description))
        return result_appeal["code"]
    
    def definition_previous_device(self, customer: Customer, device: Device):
        result = db_manager.execute("""SELECT DISTINCT d.id
                                        FROM appeals a
                                        JOIN devices d ON a.device_id = d.id
                                        JOIN types_devices td ON d.type_id = td.id
                                        WHERE a.customer_id = ? AND d.model = ?""", args= (customer.id, device.model))
        return result["data"][0]
    
    def load_appeals(self, customer: Customer):
        result = db_manager.execute("""SELECT a.id, d.model, a.description 
                                    FROM appeals a
                                    JOIN devices d ON a.device_id = d.id
                                    WHERE a.customer_id = ? AND NOT EXISTS (
                                                                SELECT 1
                                                                FROM claims cl
                                                                WHERE cl.appeal_id = a.id
                                                                )""", (customer.id,), many=True)
        return result["data"]
    
    def load_claims(self, customer: Customer):
        result = db_manager.execute("""SELECT c.id, c.start_date, d.model, a.description, s.name 
                                        FROM claims c
                                        JOIN appeals a ON c.appeal_id = a.id
                                        JOIN devices d ON a.device_id = d.id
                                        JOIN statuses s ON c.status_id = s.id
                                        WHERE a.customer_id = ?""", (customer.id,), many=True)
        return result["data"]
    
    def load_information_customer(self, customer: Customer):
        result = db_manager.execute("""SELECT FIO, address, number_phone, email FROM customers WHERE id = ?""", (customer.id,))
        return result["data"]
    
    def update_full_information_customer(self, customer: Customer):
        result = db_manager.execute("""UPDATE customers SET FIO = ?, address = ?, number_phone = ?, email = ? WHERE id = ?""", args= (customer.FIO, customer.address, customer.number_phone, customer.email, customer.id))
        return result["code"]
    
    def checking_сurrent_client_password(self, customer: Customer,  user: User):
        result = db_manager.execute("""SELECT u.id
                                        FROM customers c
                                        JOIN users u ON c.user_id = u.id
                                        WHERE c.id = ? AND u.password = ?""", args= (customer.id, user.password))
        return result["data"]
    
    def update_current_client_password(self, customer: Customer,  user: User):
        result = db_manager.execute("""UPDATE users SET password = ?
                                        WHERE id = (
                                        SELECT u.id
                                        FROM customers c
                                        JOIN users u ON c.user_id = u.id
                                        WHERE c.id = ?);""", args= (user.password, customer.id))
        return result["code"]
    
    def load_all_appeals(self):
        result = db_manager.execute("""SELECT a.id, c.FIO, d.model, a.description
                                        FROM appeals a
                                        JOIN devices d ON a.device_id = d.id
                                        JOIN customers c ON a.customer_id = c.id
                                        WHERE NOT EXISTS (
                                                SELECT 1
                                                FROM claims cl
                                                WHERE cl.appeal_id = a.id
                                                )""", many= True)
        return result["data"]
    
    def load_all_claims(self):
        result = db_manager.execute("""SELECT c.id, cus.FIO, d.model, a.description, c.start_date, c.end_date, s.name
                                        FROM claims c
                                        JOIN appeals a ON c.appeal_id = a.id
                                        JOIN devices d ON a.device_id = d.id
                                        JOIN customers cus ON a.customer_id = cus.id
                                        JOIN statuses s ON c.status_id = s.id""", many= True)
        return result["data"]
    
    def load_all_customers(self):
        result = db_manager.execute("""SELECT id, FIO, address, number_phone, email FROM customers""", many= True)
        return result["data"]
    
    def create_claim_from_appeal(self, appeal: Appeal):
        result = db_manager.execute("""INSERT INTO claims (appeal_id) VALUES (?)""", args= (appeal.id,))
        return result["code"]

    def delete_appeal(self, appeal: Appeal):
        result = db_manager.execute("""DELETE FROM appeals WHERE id = ?""", args= (appeal.id,))
        return result["code"]
    
    def load_all_contracts(self):
        result = db_manager.execute("""SELECT 
                                        contracts.id AS contract_id,
                                        employees.FIO AS employee_name,
                                        claims.id AS claim_id,
                                        contracts.description_work_done AS work_description,
                                        contracts.cost AS cost,
                                        GROUP_CONCAT(components.name, ', ') AS used_tools
                                        FROM contracts
                                        JOIN 
                                        employees ON contracts.employee_id = employees.id
                                        JOIN 
                                        claims ON contracts.claim_id = claims.id
                                        LEFT JOIN 
                                        components_used ON contracts.id = components_used.contract_id
                                        LEFT JOIN 
                                        components ON components_used.component_id = components.id
                                        GROUP BY 
                                        contracts.id""", many= True)
        return result["data"]
    
    def load_all_masters(self):
        result = db_manager.execute("""SELECT e.FIO FROM employees e
                                        JOIN posts p ON e.post_id = p.id
                                        WHERE p.name = 'Мастер' """, many= True)
        return result["data"]
    
    def employee_definition(self, employee: Employee) -> int:
        result = db_manager.execute("""SELECT id FROM employees WHERE FIO = ?""", args= (employee.FIO,))
        return result["data"][0]

    def create_contract(self, contract: Contract):
        result = db_manager.execute("""INSERT INTO contracts (claim_id, employee_id, cost) VALUES (?, ?, ?)""", args= (contract.claim_id, contract.employee_id, contract.cost))
        return result["code"]
    
    def load_statuses(self):
        result = db_manager.execute("""SELECT name FROM statuses""", many= True)
        return result["data"]
    
    def status_definition(self, status: Status) -> int:
        result = db_manager.execute("""SELECT id FROM statuses WHERE name = ?""", args= (status.name,))
        return result["data"][0]
    
    def update_status_in_claim(self, claim: Claim):
        result = db_manager.execute("""UPDATE claims SET status_id = ? WHERE id = ?""", args= (claim.status_id, claim.id))
        return result["code"]
    
    def update_description_in_contract(self, contract: Contract):
        result = db_manager.execute("""UPDATE contracts SET description_work_done = ? WHERE id = ?""", args= (contract.description_work_done, contract.id))
        return result["code"]

    def tool_definition(self, tool: Tool) -> int:
        result = db_manager.execute("""SELECT id FROM components WHERE name = ?""", args= (tool.name,))
        return result["data"][0]
    
    def load_components(self):
        result = db_manager.execute("""SELECT name FROM components""", many= True)
        return result["data"]
    
    def add_component(self, toolused: ToolUsed):
        result = db_manager.execute("""INSERT INTO components_used (contract_id, component_id) VALUES (?, ?)""", args= (toolused.contract_id, toolused.tool_id))
        return result["code"]
    
main_functions = MainFunctions(db_manager)