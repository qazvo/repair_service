from database.db_manager import db_manager
from client.main_elements import User, main_functions

print(main_functions.check_login_user(User(login="ccasda")))