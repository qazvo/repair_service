import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'repair_service.db')
 
class DBManager:
    def __init__(self, default_path: str) -> None:
        self.default_path = default_path
    
    def connect_to_db(self) -> tuple[sqlite3.Connection, sqlite3.Cursor]:
        conn = sqlite3.connect(self.default_path)
        cur = conn.cursor()
        return conn, cur
    
    def check_base(self) -> bool:
        return os.path.exists(self.default_path)
    
    def create_base(self, script_tables_path: str, script_data_path: str):
        conn, cur = self.connect_to_db()
        try:
            cur.executescript(open(script_tables_path, encoding= 'utf-8').read())
            cur.executescript(open(script_data_path, encoding= 'utf-8').read())
            conn.commit()
            conn.close()
        except sqlite3.Error as ex:
            print(ex)
            os.remove(self.db_path)

    def execute(self, query: str, args: tuple = (), many: bool = False) -> dict:
        conn, cur = self.connect_to_db()
        try: 
            res = cur.execute(query, args)
            if many:
                result = res.fetchall()
            else:
                result = res.fetchone()
        except sqlite3.Error as err:
            conn.close()
            return {"code": 400, "msg": str(err), "error": True, "data": None}
        conn.commit()
        conn.close()
        return {"code": 200, "msg": "Successfully", "error": False, "data": result}

db_manager = DBManager(default_path=DB_PATH)
    