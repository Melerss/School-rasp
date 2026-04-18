import sqlite3
from config import DATABASE

class DB_Manager:
    def __init__(self, database):
        self.database = database
        
    def create_tables(self):
        conn = sqlite3.connect(self.database)
        with conn:
            conn.execute('''CREATE TABLE IF NOT EXISTS users( 
                        telegramm_id INTEGER PRIMARY KEY AUTOINCREMENT, 
                        class TEXT NOT NULL);
                        ''')
    
            conn.execute('''CREATE TABLE IF NOT EXISTS Lessens (
                        id INTEGER PRIMARY KEY AUTOINCREMENT, 
                        weekend TEXT NOT NULL,
                        number_lessen INTEGER NOT NULL,
                        name_lessen TEXT NOT NULL,
                        time_start TEXT NOT NULL,
                        time_end TEXT NOT NULL,
                        class TEXT NOT NULL); 
                        ''')

    def __executemany(self, sql, data):
        conn = sqlite3.connect(self.database)
        conn.executemany(sql, data)
        conn.commit()
        conn.close()
    
    def __select_data(self, sql, data = tuple()):
        conn = sqlite3.connect(self.database)
        with conn:
            cur = conn.cursor()
            cur.execute(sql, data)
            return cur.fetchall()
    
    def add_user(self, telegramm_id, class_name):
        sql = "SELECT * FROM users WHERE telegramm_id = ?"  
        res = self.__select_data(sql, (telegramm_id,))
        if not res:
            sql = "INSERT INTO users (telegramm_id, class) VALUES (?,?)"
            self.__executemany(sql, ((telegramm_id, class_name),))
            return True
        return False
    
    def add_lessen(self, weekend, number_lessen, name_lessen, time_start, time_end, class_name):
        sql = "INSERT INTO Lessens (weekend, number_lessen, name_lessen, time_start, time_end, class) VALUES (?, ?, ?, ?, ?, ?)"
        self.__executemany(sql, [(weekend, number_lessen, name_lessen, time_start, time_end, class_name)])
        return True   
       
    def return_lessens(self, class_name):
        sql = "SELECT * FROM Lessens WHERE class = ?" 
        return self.__select_data(sql, (class_name,))
    
    def get_class(self, telegramm_id):
        sql = "SELECT class FROM users WHERE telegramm_id = ?"  
        result = self.__select_data(sql, (telegramm_id,))
        if result:
            return result[0][0] 
        return None

if __name__ == '__main__':
    manager = DB_Manager(DATABASE)
    manager.create_tables()

    