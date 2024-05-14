from db_manager import db_manager
import os 

script_tables = os.path.join(os.path.dirname(__file__), 'scripts', 'db.sql')
script_data = os.path.join(os.path.dirname(__file__), 'scripts', 'data.sql')

db_manager.create_base(script_tables_path = script_tables, script_data_path = script_data)