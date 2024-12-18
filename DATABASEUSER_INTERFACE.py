import sqlite3

class UserDatabaseInterface:
    def __init__(self):
        # Connect to the database (or create it if it doesn't exist)
        self.connection = sqlite3.connect("library.db")
        self.cursor = self.connection.cursor()

        # Create users table if it doesn't exist
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
        """Fetch a user by first and last name."""
        self.cursor.execute("SELECT * FROM users WHERE first_name = ? AND last_name = ?", (first_name, last_name))
        return self.cursor.fetchone()

    def add_user(self, first_name, last_name, email):
        """Add a new user to the database."""
        self.cursor.execute("INSERT INTO users (first_name, last_name, email, books_issued) VALUES (?, ?, ?, ?)", 
                            (first_name, last_name, email, 0))
        self.connection.commit()

    def issue_book(self, user_id):
        """Increase the number of books issued to a user."""
        self.cursor.execute("UPDATE users SET books_issued = books_issued + 1 WHERE id = ?", (user_id,))
        self.connection.commit()

    def return_book(self, user_id):
        """Decrease the number of books issued to a user."""
        self.cursor.execute("UPDATE users SET books_issued = books_issued - 1 WHERE id = ?", (user_id,))
        self.connection.commit()
    
    def fetch_all_users(self):
        """Fetch all users in the database."""
        self.cursor.execute("SELECT * FROM users")
        return self.cursor.fetchall()
    

    def wipe_all_users(self):
        """Delete all users from the database (wipe all data)."""
        self.cursor.execute("DELETE FROM users")
        self.connection.commit()

    def close(self):
        """Close the database connection."""
        self.connection.close()
    
# Example usage
user_db = UserDatabaseInterface()

# Add a new user (example)


# Fetch and print all users
users = user_db.fetch_all_users()
for user in users:
    print(user)

# Close the connection
user_db.close()


