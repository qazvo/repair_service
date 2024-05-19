from database.db_manager import db_manager

print(db_manager.execute("""INSERT INTO users (login, password, type_id) VALUES ('ВАФЫВвыф', 'авываываыв', 1)"""))