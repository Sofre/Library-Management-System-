import customtkinter as ctk
from PIL import Image
from DATABASE_CREDENTIALS import Database_CREDI  
from LMS_LIB_MENU import MenuWindow
from resource_manager import load_image, get_db_connection  


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("600x500")
        self.title("Library Management System")
        
        
        png_image = load_image("online-library.png")  
        
        # Save the image as .ico for the window icon
        png_image.save('D:/LMS/Library-Management-System-/IMG/online-library.ico', format='ICO')
        self.iconbitmap('D:/LMS/Library-Management-System-/IMG/online-library.ico')
        
        ctk.set_appearance_mode("automatic")
        ctk.set_default_color_theme("dark-blue")  
        
        self.configure(bg="#1E2A47") 

     
        self.db = Database_CREDI()
        self.db.filename = get_db_connection("dataCRED.txt")  

    
        self.image = ctk.CTkImage(
            light_image=load_image("LMS-removebg-preview.png"),
            dark_image=load_image("LMS-removebg-preview.png"),
            size=(350, 175))  

        self.image_label = ctk.CTkLabel(self, image=self.image, text="")
        self.image_label.place(relx=0.5, rely=0.15, anchor="center")

        # Buttons for login and registration
        self.button = ctk.CTkButton(self, text="LOG IN", command=self.button_callback, corner_radius=20, width=200, height=40, fg_color="#005D99", hover_color="#004C80")
        self.button.place(relx=0.5, rely=0.45, anchor="center")

        self.button_1 = ctk.CTkButton(self, text="REGISTER", command=self.open_register_window, corner_radius=20, width=200, height=40, fg_color="#005D99", hover_color="#004C80")
        self.button_1.place(relx=0.5, rely=0.55, anchor="center")

        self.email_entry = ctk.CTkEntry(self, placeholder_text="Email Address", width=350, height=40, fg_color="#2E3B56", border_color="#005D99", text_color="white")
        self.email_entry.place(relx=0.5, rely=0.75, anchor="center")

        self.password_entry = ctk.CTkEntry(self, placeholder_text="Password", show="*", width=350, height=40, fg_color="#2E3B56", border_color="#005D99", text_color="white")
        self.password_entry.place(relx=0.5, rely=0.85, anchor="center")

        self.author_label = ctk.CTkLabel(self, text="© 2024, Developed by инг. Душко Софрониевски", font=("Arial", 12), text_color="gray")
        self.author_label.place(relx=0.5, rely=0.98, anchor="center")

        self.toplevel_window = None

        
        self.optionmenu = ctk.CTkOptionMenu(self, values=["DARK", "LIGHT", "AUTOMATIC"], command=self.optionmenu_callback)
        self.optionmenu.set("AUTOMATIC")
        self.optionmenu.place(relx=0.95, rely=0.05, anchor="ne", x=12, y=10)

    def optionmenu_callback(self, selected_value):
       
        match(selected_value):
            case "DARK": 
                ctk.set_appearance_mode("dark")
            case "LIGHT": 
                ctk.set_appearance_mode("light")
            case "AUTOMATIC": 
                ctk.set_appearance_mode("system")

    def button_callback(self):
      
        print("Log In button clicked")
        email = self.email_entry.get()
        password = self.password_entry.get()

        if self.db.check(email, password):
            print("Login successful!")
            self.open_main_window() 
        else:
            print("Invalid credentials")
            self.error_login_window()

    def open_register_window(self):
      
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = self.register_window()
        else:
            self.toplevel_window.focus()

    def open_main_window(self):
        
        self.withdraw()  
        main_window = MenuWindow()  
        main_window.mainloop()  

    def error_login_window(self):
       
        self.error_log_window = ctk.CTkToplevel(self)
        self.error_log_window.geometry("400x300")
        self.error_log_window.title("ERROR")
        self.text_login = ctk.CTkLabel(self.error_log_window, text="ERROR 201: Invalid credentials!", font=("Arial", 20), text_color="white")
        self.text_login.place(relx=0.5, rely=0.5, anchor="center")

    def register_window(self):
        
        self.registration_window = ctk.CTkToplevel(self)
        self.registration_window.geometry("400x300")
        self.registration_window.title("Register")

        self.registration_email_entry = ctk.CTkEntry(self.registration_window, placeholder_text="Email Address", width=300, height=40, fg_color="#2E3B56", border_color="#005D99", text_color="white")
        self.registration_email_entry.pack(padx=20, pady=10)

        self.registration_password_entry = ctk.CTkEntry(self.registration_window, placeholder_text="Password", show="*", width=300, height=40, fg_color="#2E3B56", border_color="#005D99", text_color="white")
        self.registration_password_entry.pack(padx=20, pady=10)

        self.register_button = ctk.CTkButton(self.registration_window, text="Register", command=self.register_user, corner_radius=20, width=150, height=40, fg_color="#005D99", hover_color="#004C80")
        self.register_button.pack(padx=20, pady=20)

    def register_user(self):
       
        email = self.registration_email_entry.get()
        password = self.registration_password_entry.get()
        self.db.insert(email, password)
        print(f"Registered: Email: {email}, Password: {password}")
        self.db.save_to_file()
        self.registration_window.destroy()



if __name__ == "__main__":
    app = App()
    app.mainloop()
