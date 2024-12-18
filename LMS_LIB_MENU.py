import customtkinter as ctk
from PIL import Image, ImageTk
from LMS_LIB_VIEW import ViewWindow
from LMS_LIB_ADDBK import AddBookWindow
from LMS_LIB_ADDSUSR import UserRegistrationWindow
from LMS_LIB_ISSUE import IssueBookWindow
from LMS_LIB_ADMIN   import WipeDataWindow  # Assuming you've saved the WipeDataWindow class

class MenuWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("800x600")
        self.title("Library Dashboard")
        ctk.set_appearance_mode("dark")
        
        png_image = Image.open("D:/LMS/Library-Management-System-/IMG/online-library.png")
        png_image.save('D:/LMS/Library-Management-System-/IMG/online-library.ico', format='ICO')
        self.iconbitmap('D:/LMS/Library-Management-System-/IMG/online-library.ico')

        # Title label for the window
        self.label = ctk.CTkLabel(self, text="Welcome to the Library Dashboard!", font=("Arial", 30), text_color="grey")
        self.label.place(relx=0.5, rely=0.1, anchor="center")

        # Buttons for different functionalities
        self.view_books_button = ctk.CTkButton(self, text="View Books", command=self.button_callback_VBook, corner_radius=20, width=200, height=40, fg_color="#005D99", hover_color="#004C80")
        self.view_books_button.place(relx=0.5, rely=0.3, anchor="center")

        self.issue_book_button = ctk.CTkButton(self, text="Issue Book", command=self.button_callback_IBook, corner_radius=20, width=200, height=40, fg_color="#005D99", hover_color="#004C80")
        self.issue_book_button.place(relx=0.5, rely=0.4, anchor="center")

        self.add_book_button = ctk.CTkButton(self, text="Add Book", command=self.button_callback_ABook, corner_radius=20, width=200, height=40, fg_color="#005D99", hover_color="#004C80")
        self.add_book_button.place(relx=0.5, rely=0.5, anchor="center")

        self.inform_student_button = ctk.CTkButton(self, text="Register User", command=self.button_callback_ADDSTUDENT, corner_radius=20, width=200, height=40, fg_color="#005D99", hover_color="#004C80")
        self.inform_student_button.place(relx=0.5, rely=0.6, anchor="center")

        # Wipe Data button to open the wipe data window
        self.wipe_data_button = ctk.CTkButton(self, text="ADMIN", command=self.button_callback_WipeData, corner_radius=20, width=200, height=40, fg_color="#E52B50", hover_color="#C41E3A")
        self.wipe_data_button.place(relx=0.5, rely=0.7, anchor="center")

     

        self.author_label = ctk.CTkLabel(self, text="© 2024, Developed by инг. Душко Софрониевски", font=("Arial", 12), text_color="gray")
        self.author_label.place(relx=0.5, rely=0.98, anchor="center")

    def button_callback_VBook(self):
        """Button callback to view books."""
        print("OPENING VIEW WINDOW")
        self.bootkick_view_window()

    def bootkick_view_window(self):
        """Open the View Books window."""
        self.withdraw()  # Hide the current menu window
        main_window = ViewWindow(root_window=self)  # Pass the menu window to ViewWindow
        main_window.mainloop()

    def button_callback_IBook(self):
        """Button callback to issue a book."""
        print("OPENING ISSUE BOOK WINDOW")
        self.bootkick_issue_window()

    def bootkick_issue_window(self):
        """Open the Issue Book window."""
        self.withdraw()  # Hide the current menu window
        issue_book_window = IssueBookWindow(root_window=self)  # Pass the menu window to IssueBookWindow
        issue_book_window.mainloop()

    def button_callback_ADDSTUDENT(self):
        """Button callback to register a new user."""
        print("OPENING REGISTER USER WINDOW")
        self.bootkick_register_user_window()

    def bootkick_register_user_window(self):
        """Open the Register User window."""
        self.withdraw()  # Hide the current menu window
        user_registration_window = UserRegistrationWindow(root_window=self)  # Pass the menu window to UserRegistrationWindow
        user_registration_window.mainloop()

    def button_callback_ABook(self):
        """Button callback to add a new book."""
        print("OPENING ADD BOOK WINDOW")
        self.bootkick_add_window()

    def bootkick_add_window(self):
        """Open the Add Book window."""
        self.withdraw()  # Hide the current menu window
        add_book_window = AddBookWindow(root_window=self)  # Pass the menu window to AddBookWindow
        add_book_window.mainloop()

    def button_callback_HELP(self):
        """Button callback for Admin help."""
        print("OPENING ADMIN HELP WINDOW")
        self.bootkick_admin_help_window()

    def bootkick_admin_help_window(self):
        """Open the Admin Help window (if needed)."""
        # You can create a new help window here or show information
        print("Admin help window functionality not implemented yet.")
        # Example: self.withdraw() and open a new help window
        # help_window = AdminHelpWindow(root_window=self)
        # help_window.mainloop()

    def button_callback_WipeData(self):
        """Button callback to open the Wipe Data window."""
        print("OPENING WIPE DATA WINDOW")
        self.bootkick_wipe_data_window()

    def bootkick_wipe_data_window(self):
        """Open the Wipe Data window."""
        self.withdraw()  # Hide the current menu window
        wipe_data_window = WipeDataWindow(book_db_path="books.db", user_db_path="library.db")  # Pass the paths to WipeDataWindow
        wipe_data_window.mainloop()


if __name__ == "__main__":
    menu = MenuWindow()  # This initializes the MenuWindow
    menu.mainloop()


