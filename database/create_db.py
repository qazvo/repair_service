from db_manager import db_manager, DB_PATH

script_tables = "D:/Program/Programing/Projects/repair_service/database/scripts/db.sql"
script_data = "D:/Program/Programing/Projects/repair_service/database/scripts/data.sql"
db_manager.create_base(script_tables_path = script_tables, script_data_path = script_data)