import customtkinter as ctk
from DATABASEBK_INTERFACE import DatabaseInterface
from DATABASEUSER_INTERFACE import UserDatabaseInterface

class IssueBookWindow(ctk.CTk):
    def __init__(self, root_window):
        super().__init__()
        self.root_window = root_window
        self.geometry("800x600")  # Increased height to accommodate additional fields
        self.title("Issue Book")
        ctk.set_appearance_mode("dark")

        # Initialize the database interfaces
        self.book_db = DatabaseInterface()
        self.user_db = UserDatabaseInterface()

        self.label = ctk.CTkLabel(self, text="Issue book from Library Managment System", font=("Arial", 30),text_color="grey")
        self.label.place(relx=0.5, rely=0.1, anchor="center")

        # Book Title Fields
        self.book_title_label = ctk.CTkLabel(self, text="Enter Book Title:")
        self.book_title_label.place(relx=0.2, rely=0.2, anchor="w")

        self.book_title_entry = ctk.CTkEntry(self)
        self.book_title_entry.place(relx=0.5, rely=0.2, anchor="center")

        # First Name Fields
        self.first_name_label = ctk.CTkLabel(self, text="Enter First Name:")
        self.first_name_label.place(relx=0.2, rely=0.3, anchor="w")

        self.first_name_entry = ctk.CTkEntry(self)
        self.first_name_entry.place(relx=0.5, rely=0.3, anchor="center")

        # Last Name Fields
        self.last_name_label = ctk.CTkLabel(self, text="Enter Last Name:")
        self.last_name_label.place(relx=0.2, rely=0.4, anchor="w")

        self.last_name_entry = ctk.CTkEntry(self)
        self.last_name_entry.place(relx=0.5, rely=0.4, anchor="center")

        # Issue and Cancel Buttons
        self.issue_button = ctk.CTkButton(self, text="Issue Book", command=self.issue_book, corner_radius=10, width=200, height=40, fg_color="#005D99", hover_color="#004C80")
        self.issue_button.place(relx=0.5, rely=0.6, anchor="center")

        self.cancel_button = ctk.CTkButton(self, text="Cancel", command=self.cancel, corner_radius=10, width=200, height=40, fg_color="#E52B50", hover_color="#C41E3A")
        self.cancel_button.place(relx=0.5, rely=0.75, anchor="center")

        self.author_label = ctk.CTkLabel(self, text="© 2024, Developed by инг. Душко Софрониевски", font=("Arial", 12), text_color="gray")
        self.author_label.place(relx=0.5, rely=0.98, anchor="center")

    def cancel(self):
        """Cancel the book issuing and return to the main menu."""
        self.destroy()
        if self.root_window:
            self.root_window.deiconify()  # Re-show the main menu

    def issue_book(self):
        book_title = self.book_title_entry.get()
        first_name = self.first_name_entry.get()
        last_name = self.last_name_entry.get()

        if not book_title or not first_name or not last_name:
            print("Please enter book title, first name, and last name.")
            return

        # Search for the book in the database
        books = self.book_db.search_books(book_title)
        if not books:
            print(f"Book titled '{book_title}' not found.")
            return

        book = books[0]  # Assume the first match is the desired book

        # Check if 'available' key exists and if it's 0 (book is unavailable)
        if 'available' not in book:
            print("The 'available' field is missing in the book data.")
            return

        if book['available'] == 0:
            print(f"Sorry, '{book_title}' is currently unavailable.")
            self.show_already_issued_popup(book_title)
            return

        # Fetch the user from the database
        user = self.user_db.fetch_user_by_name(first_name, last_name)
        if not user:
            print(f"User '{first_name} {last_name}' not found.")
            return

        # Check if the user already has any books issued
        if user[3] > 0:  # user[3] is the 'books_issued' field in the user database
            print(f"User '{first_name} {last_name}' has already issued books and cannot issue another.")
            self.show_already_issued_popup(book_title)
            return

        # Issue the book to the user
        self.user_db.issue_book(user[0])  # user[0] is the user ID
        self.book_db.issue_book(book['id'])  # book['id'] is the book ID, mark it as issued

        print(f"Book '{book_title}' has been issued to user '{first_name} {last_name}'.")

        # Show pop-up confirmation
        self.show_popup(book_title, first_name, last_name)

        # Close the window and return to the main menu
        self.cancel()

    def show_popup(self, book_title, first_name, last_name):
        """Show a pop-up window with the confirmation message."""
        popup = ctk.CTkToplevel(self)  # Create a new top-level window (pop-up)
        popup.geometry("300x150")
        popup.title("Book Issued")

        # Display the message in the pop-up window
        message = f"Book '{book_title}' has been issued to user '{first_name} {last_name}'."
        label = ctk.CTkLabel(popup, text=message, font=("Arial", 14))
        label.pack(pady=20)

        # Close button for the pop-up window
        close_button = ctk.CTkButton(popup, text="Close", command=popup.destroy)
        close_button.pack(pady=10)

    def show_already_issued_popup(self, book_title):
        """Show a pop-up window indicating that the book is already issued to a user."""
        popup = ctk.CTkToplevel(self)  # Create a new top-level window (pop-up)
        popup.geometry("300x150")
        popup.title("Action Failed")

        # Display the message in the pop-up window
        message = f"Book '{book_title}' is already issued and unavailable."
        label = ctk.CTkLabel(popup, text=message, font=("Arial", 14))
        label.pack(pady=20)

        # Close button for the pop-up window
        close_button = ctk.CTkButton(popup, text="Close", command=popup.destroy)
        close_button.pack(pady=10)



    def on_back_button_click(self):
        
        if self.root_window:
            self.destroy()  # Close the current window
            self.root_window.deiconify()  # Show the root window (assuming it's hidden)

if __name__ == "__main__":
    isu = IssueBookWindow(root_window=None)  # Replace `None` with the actual root window  
    isu.mainloop()


