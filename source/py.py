from database.db_manager import db_manager

db_manager.execute("""INSERT INTO claims (appeal_id, status_id) VALUES (3,1)""")