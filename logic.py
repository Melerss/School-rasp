import sqlite3
from config import DATABASE

class DB_Manager:
    def __init__(self, database):
        self.database = database
        
    def create_tables(self):
        conn = sqlite3.connect(self.database)
        with conn:
            conn.execute('''CREATE TABLE users( 
                        telegramm_id INTEGER PRIMARY KEY, 
                        class TEXT NOT NULL);
                          
                        ''') 
    
            conn.execute('''CREATE TABLE Lessens (
                        id INTEGER, weekend TEXT NOT NULL,
                        number_lessen INTEGER NOT NULL,
                        name_lessen TEXT NOT NULL,
                        time_start TEXT NOT NULL,
                        time_end TEXT NOT NULL,
                        class TEXT NOT NULL); 
                         
                         ''')

    def __executemany(self, sql, data):
        conn = sqlite3.connect(self.database)
        with conn:
            conn.executemany(sql, data)
            conn.commit()
    
    def __select_data(self, sql, data = tuple()):
        conn = sqlite3.connect(self.database)
        with conn:
            cur = conn.cursor()
            cur.execute(sql, data)
            return cur.fetchall()
    def add_user(self, telegramm_id, class_name):
        sql = "select * FROM users WHERE telegramm_id = ?"
        res = self.__select_data(sql, (telegramm_id,))
        if not res:
            sql = "INSERT INTO users (telegramm_id, class) VALUES (?,?)"
            self.__executemany(self, sql, (telegramm_id, class_name))
            return True
        return False

    def add_lessen(self,weekend,number_lessen,name_lessen,time_start,time_end,class_name):
            sql = "INSERT INTO lessen (weekend,number_lessen,name_lessen,time_start,time_end,class) VALUES (?, ?, ?, ?, ?, ?)"
            self.__executemany(self, sql, (weekend,number_lessen,name_lessen,time_start,time_end,class_name))
            return True
    
if __name__ == '__main__':
    manager = DB_Manager(DATABASE)
    manager.create_tables()

    