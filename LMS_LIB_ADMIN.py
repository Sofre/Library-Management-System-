import sqlite3
import customtkinter as ctk
from tkinter import messagebox

# Database Interface for Books
class DatabaseInterface:
    def __init__(self, db_name="books.db"):
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()

        # Create the books table if it doesn't exist
        self.cursor.execute("PRAGMA table_info(books);")
        columns = [column[1] for column in self.cursor.fetchall()]
        
        if 'available' not in columns:
            self.cursor.execute("ALTER TABLE books ADD COLUMN available INTEGER DEFAULT 1")
            self.conn.commit()
            print("Column 'available' added to the 'books' table.")

    def clear_books(self):
        """Clears all book data from the books table."""
        try:
            self.cursor.execute("DELETE FROM books")  # Delete all records from books table
            self.conn.commit()
            print("All book records have been cleared.")
            return True
        except Exception as e:
            print(f"Error clearing books data: {e}")
            return False

    def close(self):
        """Close the database connection."""
        self.conn.close()


# Database Interface for Users
class UserDatabaseInterface:
    def __init__(self, db_name="library.db"):
        self.db_name = db_name
        self.connection = sqlite3.connect(self.db_name)
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

    def clear_users(self):
        """Clears all user data from the users table."""
        try:
            self.cursor.execute("DELETE FROM users")  # Delete all records from users table
            self.connection.commit()
            print("All user records have been cleared.")
            return True
        except Exception as e:
            print(f"Error clearing users data: {e}")
            return False

    def close(self):
        """Close the database connection."""
        self.connection.close()


# Wipe Data Window (GUI)
class WipeDataWindow(ctk.CTk):
    def __init__(self, book_db_path, user_db_path):
        super().__init__()
        self.geometry("800x600")  # Increased height for caution message
        self.title("Data Wipe Confirmation")
        self.book_db_path = book_db_path
        self.user_db_path = user_db_path

        # Caution Label
        self.caution_label = ctk.CTkLabel(self, text="CAUTION: Pressing the button will wipe all data from the library!\nThis action is irreversible!", font=("Arial", 16, "bold"), text_color="red")
        self.caution_label.place(relx=0.5, rely=0.2, anchor="center")

        # Wipe data for books button
        self.wipe_books_button = ctk.CTkButton(self, text="Wipe Books Data", command=self.wipe_books_data, fg_color="#E52B50", hover_color="#C41E3A")
        self.wipe_books_button.place(relx=0.5, rely=0.5, anchor="center")

        # Wipe data for users button
        self.wipe_users_button = ctk.CTkButton(self, text="Wipe Users Data", command=self.wipe_users_data, fg_color="#E52B50", hover_color="#C41E3A")
        self.wipe_users_button.place(relx=0.5, rely=0.6, anchor="center")

        # Cancel button
        self.cancel_button = ctk.CTkButton(self, text="Cancel", command=self.destroy, fg_color="#005D99", hover_color="#004C80")
        self.cancel_button.place(relx=0.5, rely=0.8, anchor="center")

        self.author_label = ctk.CTkLabel(self, text="© 2024, Developed by инг. Душко Софрониевски", font=("Arial", 12), text_color="gray")
        self.author_label.place(relx=0.5, rely=0.98, anchor="center")

    def wipe_books_data(self):
        """Wipe the books data and show a confirmation message."""
        db_interface = DatabaseInterface(self.book_db_path)
        result = db_interface.clear_books()

        if result:
            messagebox.showinfo("Success", "All book records have been wiped successfully.")
        else:
            messagebox.showerror("Error", "Failed to wipe book records.")
        
        db_interface.close()  # Close the database connection

    def wipe_users_data(self):
        """Wipe the users data and show a confirmation message."""
        user_db_interface = UserDatabaseInterface(self.user_db_path)
        result = user_db_interface.clear_users()

        if result:
            messagebox.showinfo("Success", "All user records have been wiped successfully.")
        else:
            messagebox.showerror("Error", "Failed to wipe user records.")
        
        user_db_interface.close()  # Close the database connection


# Sample Menu Window with Buttons to Launch the Wipe Data Window
class MenuWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("800x600")
        self.title("Library Dashboard")
        ctk.set_appearance_mode("dark")

        # Wipe Data button to open the wipe data window
        self.wipe_data_button = ctk.CTkButton(self, text="KILL SWITCH", command=self.button_callback_WipeData, corner_radius=20, width=200, height=40, fg_color="#E52B50", hover_color="#C41E3A")
        self.wipe_data_button.place(relx=0.5, rely=0.5, anchor="center")

    def button_callback_WipeData(self):
        """Open the Wipe Data window."""
        print("Opening Data Wipe Window")
        self.bootkick_wipe_data_window()

    def bootkick_wipe_data_window(self):
        """Open the wipe data window."""
        self.withdraw()  # Hide the main window
        wipe_data_window = WipeDataWindow(book_db_path="books.db", user_db_path="library.db")
        wipe_data_window.mainloop()


if __name__ == "__main__":
    menu = MenuWindow()  # This initializes the MenuWindow
    menu.mainloop()

