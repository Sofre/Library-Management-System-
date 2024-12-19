import sqlite3
import customtkinter as ctk
from tkinter import messagebox


class DatabaseInterface:
    def __init__(self, db_name="books.db"):
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()

       
        self.cursor.execute("PRAGMA table_info(books);")
        columns = [column[1] for column in self.cursor.fetchall()]
        
        if 'available' not in columns:
            self.cursor.execute("ALTER TABLE books ADD COLUMN available INTEGER DEFAULT 1")
            self.conn.commit()
            print("Column 'available' added to the 'books' table.")

    def clear_books(self):
        """Clears all book data from the books table."""
        try:
            self.cursor.execute("DELETE FROM books") 
            self.conn.commit()
            print("All book records have been cleared.")
            return True
        except Exception as e:
            print(f"Error clearing books data: {e}")
            return False

    def close(self):
        """Close the database connection."""
        self.conn.close()



class UserDatabaseInterface:
    def __init__(self, db_name="library.db"):
        self.db_name = db_name
        self.connection = sqlite3.connect(self.db_name)
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

    def clear_users(self):
       
        try:
            self.cursor.execute("DELETE FROM users")  
            self.connection.commit()
            print("All user records have been cleared.")
            return True
        except Exception as e:
            print(f"Error clearing users data: {e}")
            return False

    def close(self):
        
        self.connection.close()



class WipeDataWindow(ctk.CTk):
    def __init__(self, book_db_path, user_db_path):
        super().__init__()
        self.geometry("800x600")  
        self.title("Data Wipe Confirmation")
        self.book_db_path = book_db_path
        self.user_db_path = user_db_path

        
        self.caution_label = ctk.CTkLabel(self, text="CAUTION: Pressing the button will wipe all data from the library!\nThis action is irreversible!", font=("Arial", 16, "bold"), text_color="red")
        self.caution_label.place(relx=0.5, rely=0.2, anchor="center")

       
        self.wipe_books_button = ctk.CTkButton(self, text="Wipe Books Data", command=self.wipe_books_data, fg_color="#E52B50", hover_color="#C41E3A")
        self.wipe_books_button.place(relx=0.5, rely=0.5, anchor="center")

        
        self.wipe_users_button = ctk.CTkButton(self, text="Wipe Users Data", command=self.wipe_users_data, fg_color="#E52B50", hover_color="#C41E3A")
        self.wipe_users_button.place(relx=0.5, rely=0.6, anchor="center")

       
        self.cancel_button = ctk.CTkButton(self, text="Cancel", command=self.destroy, fg_color="#005D99", hover_color="#004C80")
        self.cancel_button.place(relx=0.5, rely=0.8, anchor="center")

        self.author_label = ctk.CTkLabel(self, text="© 2024, Developed by инг. Душко Софрониевски", font=("Arial", 12), text_color="gray")
        self.author_label.place(relx=0.5, rely=0.98, anchor="center")

    def wipe_books_data(self):
        
        db_interface = DatabaseInterface(self.book_db_path)
        result = db_interface.clear_books()

        if result:
            messagebox.showinfo("Success", "All book records have been wiped successfully.")
        else:
            messagebox.showerror("Error", "Failed to wipe book records.")
        
        db_interface.close()  

    def wipe_users_data(self):
      
        user_db_interface = UserDatabaseInterface(self.user_db_path)
        result = user_db_interface.clear_users()

        if result:
            messagebox.showinfo("Success", "All user records have been wiped successfully.")
        else:
            messagebox.showerror("Error", "Failed to wipe user records.")
        
        user_db_interface.close()  



class MenuWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("800x600")
        self.title("Library Dashboard")
        ctk.set_appearance_mode("dark")

       
        self.wipe_data_button = ctk.CTkButton(self, text="KILL SWITCH", command=self.button_callback_WipeData, corner_radius=20, width=200, height=40, fg_color="#E52B50", hover_color="#C41E3A")
        self.wipe_data_button.place(relx=0.5, rely=0.5, anchor="center")

    def button_callback_WipeData(self):
        
        print("Opening Data Wipe Window")
        self.bootkick_wipe_data_window()

    def bootkick_wipe_data_window(self):
       
        self.withdraw() 
        wipe_data_window = WipeDataWindow(book_db_path="books.db", user_db_path="library.db")
        wipe_data_window.mainloop()


if __name__ == "__main__":
    menu = MenuWindow()  
    menu.mainloop()

