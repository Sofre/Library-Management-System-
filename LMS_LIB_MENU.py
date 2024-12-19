import customtkinter as ctk
from PIL import Image
from resource_manager import load_image
from LMS_LIB_VIEW import ViewWindow
from LMS_LIB_ADDBK import AddBookWindow
from LMS_LIB_ADDSUSR import UserRegistrationWindow
from LMS_LIB_ISSUE import IssueBookWindow
from LMS_LIB_ADMIN import WipeDataWindow

class MenuWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("800x600")
        self.title("Library Dashboard")
        ctk.set_appearance_mode("dark")
        
        
        png_image = load_image("online-library.png")  
        
       
        png_image.save('D:/LMS/Library-Management-System-/IMG/online-library.ico', format='ICO')
        self.iconbitmap('D:/LMS/Library-Management-System-/IMG/online-library.ico')

       
        self.label = ctk.CTkLabel(self, text="Welcome to the Library Dashboard!", font=("Arial", 30), text_color="grey")
        self.label.place(relx=0.5, rely=0.1, anchor="center")

        self.view_books_button = ctk.CTkButton(self, text="View Books", command=self.button_callback_VBook, corner_radius=20, width=200, height=40, fg_color="#005D99", hover_color="#004C80")
        self.view_books_button.place(relx=0.5, rely=0.3, anchor="center")

        self.issue_book_button = ctk.CTkButton(self, text="Issue Book", command=self.button_callback_IBook, corner_radius=20, width=200, height=40, fg_color="#005D99", hover_color="#004C80")
        self.issue_book_button.place(relx=0.5, rely=0.4, anchor="center")

        self.add_book_button = ctk.CTkButton(self, text="Add Book", command=self.button_callback_ABook, corner_radius=20, width=200, height=40, fg_color="#005D99", hover_color="#004C80")
        self.add_book_button.place(relx=0.5, rely=0.5, anchor="center")

        self.inform_student_button = ctk.CTkButton(self, text="Register User", command=self.button_callback_ADDSTUDENT, corner_radius=20, width=200, height=40, fg_color="#005D99", hover_color="#004C80")
        self.inform_student_button.place(relx=0.5, rely=0.6, anchor="center")

        self.help_button = ctk.CTkButton(self, text="ADMIN", command=self.button_callback_admin, corner_radius=20, width=200, height=40, fg_color="#E52B50", hover_color="#C41E3A")
        self.help_button.place(relx=0.5, rely=0.8, anchor="center")

        self.author_label = ctk.CTkLabel(self, text="© 2024, Developed by инг. Душко Софрониевски", font=("Arial", 12), text_color="gray")
        self.author_label.place(relx=0.5, rely=0.98, anchor="center")

    def button_callback_VBook(self):
       
        print("OPENING VIEW WINDOW")
        self.bootkick_view_window()

    def bootkick_view_window(self):
        
        self.withdraw() 
        main_window = ViewWindow(root_window=self)  
        main_window.mainloop()

    def button_callback_IBook(self):
        """Button callback to issue a book."""
        print("OPENING ISSUE BOOK WINDOW")
        self.bootkick_issue_window()

    def bootkick_issue_window(self):
        
        self.withdraw() 
        issue_book_window = IssueBookWindow(root_window=self) 
        issue_book_window.mainloop()

    def button_callback_ADDSTUDENT(self):
       
        print("OPENING REGISTER USER WINDOW")
        self.bootkick_register_user_window()

    def bootkick_register_user_window(self):
        
        self.withdraw()  
        user_registration_window = UserRegistrationWindow(root_window=self)  
        user_registration_window.mainloop()

    def button_callback_ABook(self):
        
        print("OPENING ADD BOOK WINDOW")
        self.bootkick_add_window()

    def bootkick_add_window(self):
       
        self.withdraw()  
        add_book_window = AddBookWindow(root_window=self)  
        add_book_window.mainloop()

    def button_callback_admin(self):
        
        print("OPENING ADMIN HELP WINDOW") # TEST
        self.bootkick_admin_help_window()

    def bootkick_admin_help_window(self):
        self.withdraw()
        admin_window = WipeDataWindow(book_db_path=None , user_db_path=None)
        admin_window.mainloop()

if __name__ == "__main__":
    menu = MenuWindow()  
    menu.mainloop()



