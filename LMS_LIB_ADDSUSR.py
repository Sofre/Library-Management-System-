import customtkinter as ctk
from DATABASEUSER_INTERFACE import UserDatabaseInterface
from PIL import Image, ImageTk

class UserRegistrationWindow(ctk.CTk):
    def __init__(self, root_window, fg_color=None, **kwargs):
        super().__init__(fg_color, **kwargs)
        
        self.title("User Registration")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")
        
        png_image = Image.open("D:/LMS/Library-Management-System-/IMG/online-library.png")
        png_image.save('D:/LMS/Library-Management-System-/IMG/online-library.ico', format='ICO')
        self.iconbitmap('D:/LMS/Library-Management-System-/IMG/online-library.ico')
        
        # Label for the header
        self.label = ctk.CTkLabel(self, text="User Registration to Library System", font=("Arial", 25), text_color="grey")
        self.label.place(relx=0.5, rely=0.1, anchor="center")

        # Initialize User Database Interface
        self.user_db_interface = UserDatabaseInterface()

        # Root window reference
        self.root_window = root_window

        # Set the window size
        self.geometry("800x600")  # Increased height to accommodate back button

        # First Name entry field
        self.first_name_label = ctk.CTkLabel(self, text="First Name:", corner_radius=10, width=200)
        self.first_name_label.place(relx=0.5, rely=0.25, anchor="center")
        self.first_name_entry = ctk.CTkEntry(self, corner_radius=10, width=200)
        self.first_name_entry.place(relx=0.5, rely=0.3, anchor="center")

        # Last Name entry field
        self.last_name_label = ctk.CTkLabel(self, text="Last Name:", corner_radius=10, width=200)
        self.last_name_label.place(relx=0.5, rely=0.45, anchor="center")
        self.last_name_entry = ctk.CTkEntry(self, corner_radius=10, width=200)
        self.last_name_entry.place(relx=0.5, rely=0.5, anchor="center")

        # Email entry field
        self.email_label = ctk.CTkLabel(self, text="Email:", corner_radius=10, width=200)
        self.email_label.place(relx=0.5, rely=0.6, anchor="center")
        self.email_entry = ctk.CTkEntry(self, corner_radius=10, width=200)
        self.email_entry.place(relx=0.5, rely=0.65, anchor="center")

        # Add User button
        self.add_user_button = ctk.CTkButton(self, text="Add User", command=self.add_user, corner_radius=10, width=200)
        self.add_user_button.place(relx=0.5, rely=0.75, anchor="center")

        # Back Button
        self.back_button = ctk.CTkButton(self, text="Cancel", command=self.on_back_button_click, corner_radius=10, width=200,fg_color="#E52B50", hover_color="#C41E3A")
        self.back_button.place(relx=0.5, rely=0.85, anchor="center")

        self.author_label = ctk.CTkLabel(self, text="© 2024, Developed by инг. Душко Софрониевски", font=("Arial", 12), text_color="gray")
        self.author_label.place(relx=0.5, rely=0.98, anchor="center")

        # Feedback label
        self.feedback_label = ctk.CTkLabel(self, text="", font=("Arial", 12), text_color="green")
        self.feedback_label.place(relx=0.5, rely=0.9, anchor="center")

    def add_user(self):
        """Add the user to the database.""" 
        first_name = self.first_name_entry.get()
        last_name = self.last_name_entry.get()
        email = self.email_entry.get()

        if first_name and last_name and email:
            self.user_db_interface.add_user(first_name, last_name, email)
            self.feedback_label.configure(text=f"User {first_name} {last_name} added successfully!")
            self.clear_entries()
        else:
            self.feedback_label.configure(text="Please enter first name, last name, and email.")

    def clear_entries(self):
        """Clear the entry fields."""
        self.first_name_entry.delete(0, ctk.END)
        self.last_name_entry.delete(0, ctk.END)
        self.email_entry.delete(0, ctk.END)

    def on_back_button_click(self):
       
        if self.root_window:
            self.destroy()  # Close the current window
            self.root_window.deiconify()  # Show the root window (assuming it's hidden)

if __name__ == "__main__":
    registration_window = UserRegistrationWindow(root_window=None)
    registration_window.mainloop()


