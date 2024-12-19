import customtkinter as ctk
from DATABASEBK_INTERFACE import DatabaseInterface
from DATABASEUSER_INTERFACE import UserDatabaseInterface

class IssueBookWindow(ctk.CTk):
    def __init__(self, root_window):
        super().__init__()
        self.root_window = root_window
        self.geometry("800x600") 
        self.title("Issue Book")
        ctk.set_appearance_mode("dark")

     
        self.book_db = DatabaseInterface()
        self.user_db = UserDatabaseInterface()

        self.label = ctk.CTkLabel(self, text="Issue book from Library Managment System", font=("Arial", 30),text_color="grey")
        self.label.place(relx=0.5, rely=0.1, anchor="center")

       
        self.book_title_label = ctk.CTkLabel(self, text="Enter Book Title:")
        self.book_title_label.place(relx=0.2, rely=0.2, anchor="w")

        self.book_title_entry = ctk.CTkEntry(self)
        self.book_title_entry.place(relx=0.5, rely=0.2, anchor="center")

    
        self.first_name_label = ctk.CTkLabel(self, text="Enter First Name:")
        self.first_name_label.place(relx=0.2, rely=0.3, anchor="w")

        self.first_name_entry = ctk.CTkEntry(self)
        self.first_name_entry.place(relx=0.5, rely=0.3, anchor="center")

      
        self.last_name_label = ctk.CTkLabel(self, text="Enter Last Name:")
        self.last_name_label.place(relx=0.2, rely=0.4, anchor="w")

        self.last_name_entry = ctk.CTkEntry(self)
        self.last_name_entry.place(relx=0.5, rely=0.4, anchor="center")

       
        self.issue_button = ctk.CTkButton(self, text="Issue Book", command=self.issue_book, corner_radius=10, width=200, height=40, fg_color="#005D99", hover_color="#004C80")
        self.issue_button.place(relx=0.5, rely=0.6, anchor="center")

        self.cancel_button = ctk.CTkButton(self, text="Cancel", command=self.cancel, corner_radius=10, width=200, height=40, fg_color="#E52B50", hover_color="#C41E3A")
        self.cancel_button.place(relx=0.5, rely=0.75, anchor="center")

        self.author_label = ctk.CTkLabel(self, text="© 2024, Developed by инг. Душко Софрониевски", font=("Arial", 12), text_color="gray")
        self.author_label.place(relx=0.5, rely=0.98, anchor="center")

    def cancel(self):
        
        self.destroy()
        if self.root_window:
            self.root_window.deiconify() 

    def issue_book(self):
        book_title = self.book_title_entry.get()
        first_name = self.first_name_entry.get()
        last_name = self.last_name_entry.get()

        if not book_title or not first_name or not last_name:
            print("Please enter book title, first name, and last name.")
            return

       
        books = self.book_db.search_books(book_title)
        if not books:
            print(f"Book titled '{book_title}' not found.")
            return

        book = books[0]  

       
        if 'available' not in book:
            print("The 'available' field is missing in the book data.")
            return

        if book['available'] == 0:
            print(f"Sorry, '{book_title}' is currently unavailable.")
            self.show_already_issued_popup(book_title)
            return

        user = self.user_db.fetch_user_by_name(first_name, last_name)
        if not user:
            print(f"User '{first_name} {last_name}' not found.")
            return

        if user[3] > 0: 
            print(f"User '{first_name} {last_name}' has already issued books and cannot issue another.")
            self.show_already_issued_popup(book_title)
            return

        
        self.user_db.issue_book(user[0])  
        self.book_db.issue_book(book['id'])  

        print(f"Book '{book_title}' has been issued to user '{first_name} {last_name}'.")

       
        self.show_popup(book_title, first_name, last_name)

        
        self.cancel()

    def show_popup(self, book_title, first_name, last_name):
     
        popup = ctk.CTkToplevel(self) 
        popup.geometry("300x150")
        popup.title("Book Issued")

     
        message = f"Book '{book_title}' has been issued to user '{first_name} {last_name}'."
        label = ctk.CTkLabel(popup, text=message, font=("Arial", 14))
        label.pack(pady=20)

      
        close_button = ctk.CTkButton(popup, text="Close", command=popup.destroy)
        close_button.pack(pady=10)

    def show_already_issued_popup(self, book_title):
      
        popup = ctk.CTkToplevel(self)  
        popup.geometry("300x150")
        popup.title("Action Failed")

       
        message = f"Book '{book_title}' is already issued and unavailable."
        label = ctk.CTkLabel(popup, text=message, font=("Arial", 14))
        label.pack(pady=20)

        
        close_button = ctk.CTkButton(popup, text="Close", command=popup.destroy)
        close_button.pack(pady=10)



    def on_back_button_click(self):
        
        if self.root_window:
            self.destroy()  
            self.root_window.deiconify()  

if __name__ == "__main__":
    isu = IssueBookWindow(root_window=None)  
    isu.mainloop()


