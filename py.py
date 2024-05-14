from database.db_manager import db_manager
from client.main_elements import User, main_functions

print(db_manager.execute("""INSERT INTO users (login, password, type_id) VALUES (1, 1, 4)"""))