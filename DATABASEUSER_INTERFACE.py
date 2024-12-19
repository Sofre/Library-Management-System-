import sqlite3

class UserDatabaseInterface:
    def __init__(self):
      
        self.connection = sqlite3.connect("library.db")
        self.cursor = self.connection.cursor()

       
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT,
                last_name TEXT,
                email TEXT,
                books_issued INTEGER DEFAULT 0
            )
        """)

    def fetch_user_by_name(self, first_name, last_name):
        
        self.cursor.execute("SELECT * FROM users WHERE first_name = ? AND last_name = ?", (first_name, last_name))
        return self.cursor.fetchone()

    def add_user(self, first_name, last_name, email):
        
        self.cursor.execute("INSERT INTO users (first_name, last_name, email, books_issued) VALUES (?, ?, ?, ?)", 
                            (first_name, last_name, email, 0))
        self.connection.commit()

    def issue_book(self, user_id):
        
        self.cursor.execute("UPDATE users SET books_issued = books_issued + 1 WHERE id = ?", (user_id,))
        self.connection.commit()

    def return_book(self, user_id):
       
        self.cursor.execute("UPDATE users SET books_issued = books_issued - 1 WHERE id = ?", (user_id,))
        self.connection.commit()
    
    def fetch_all_users(self):
        
        self.cursor.execute("SELECT * FROM users")
        return self.cursor.fetchall()
    

    def wipe_all_users(self):
     
        self.cursor.execute("DELETE FROM users")
        self.connection.commit()

    def close(self):
        
        self.connection.close()
    

user_db = UserDatabaseInterface()




# TEST
users = user_db.fetch_all_users() 
for user in users:
    print(user)


user_db.close()


