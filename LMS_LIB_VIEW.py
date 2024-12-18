import customtkinter as ctk
import webbrowser
from DATABASEBK_INTERFACE import DatabaseInterface
from PIL import Image, ImageTk

class ViewWindow(ctk.CTk):
    def __init__(self, root_window, fg_color=None, **kwargs):
        super().__init__(fg_color, **kwargs)
        self.geometry('800x600')  # Default window size
        self.title("View Books")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")
        png_image = Image.open("D:/LMS/Library-Management-System-/IMG/online-library.png")


        png_image.save('D:/LMS/Library-Management-System-/IMG/online-library.ico', format='ICO')


        self.iconbitmap('D:\LMS\Library-Management-System-\IMG\online-library.ico')
        
        # Window Background Color
        self.configure(bg="#2E3B56")  # Dark background for the window

        # Initialize Database Interface
        self.db_interface = DatabaseInterface()

        # Root window reference
        self.root_window = root_window
        
        # Setup grid layout for the entire window
        self.grid_rowconfigure(0, weight=1, uniform="equal")
        self.grid_rowconfigure(1, weight=6, uniform="equal")
        self.grid_rowconfigure(2, weight=1, uniform="equal")
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Search field
        self.search_field = ctk.CTkEntry(self, corner_radius=20, placeholder_text="Search", placeholder_text_color="grey", width=150, height=40, fg_color="#2E3B56", border_color="#005D99")
        self.search_field.grid(row=0, column=1, padx=20, pady=10, sticky="ew")

        # Option menu for sorting
        self.sort_option_menu = ctk.CTkOptionMenu(self, values=("ALL", "TITLE(A-Z)", "AUTHOR(A-Z)", "RATINGS(1-5)"), width=200, height=28, button_hover_color="dark blue", command=self.sort_books_command)
        self.sort_option_menu.grid(row=0, column=0, padx=20, pady=10, sticky="ew")

        # Table frame (placed inside a scrollable canvas)
        self.table_frame_canvas = ctk.CTkCanvas(self, bg="#2E3B56")  # Set canvas background color to match window
        self.table_frame_canvas.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        # Scrollbar
        self.table_scrollbar = ctk.CTkScrollbar(self.table_frame_canvas, orientation="vertical", command=self.table_frame_canvas.yview)
        self.table_scrollbar.grid(row=0, column=1, sticky="ns")
        self.table_frame_canvas.configure(yscrollcommand=self.table_scrollbar.set)

        # Frame inside the canvas where rows will be placed
        self.table_frame = ctk.CTkFrame(self.table_frame_canvas, corner_radius=10, fg_color="#2E3B56", border_color="#005D99")
        self.table_frame.grid(row=0, column=0, sticky="nsew")

        # Back button
        self.back_button = ctk.CTkButton(self, text="Cancel", command=self.on_back_button_click, width=120,fg_color="#E52B50",hover_color="#C41E3A")
        self.back_button.grid(row=2, column=0, columnspan=2, pady=20, sticky="nsew")

        # Footer
        self.author_label = ctk.CTkLabel(self, text="© 2024, Developed by инг. Душко Софрониевски", font=("Arial", 12), text_color="gray")
        self.author_label.grid(row=3, column=0, columnspan=2, pady=10, sticky="s")

        # Fetch books from the database
        self.books = self.db_interface.fetch_books()

        # Initial population of the table
        self.populate_table(self.books)

        # Bind the search functionality
        self.search_field.bind("<KeyRelease>", self.search_books)

    def populate_table(self, books):
        """Populate the table with books data."""
        # Clear existing content
        for widget in self.table_frame.winfo_children():
            widget.destroy()

        # Create table headers
        self.create_table_header()

        # Create table rows
        row_font = ('Arial', int(self.winfo_width() / 4000))  # Dynamically scale font size based on window width
        for row_idx, book in enumerate(books, start=1):
            self.create_table_row(row_idx, book["title"], book["author"], book["rating"], row_font)

        # Update the canvas scrolling region
        self.table_frame_canvas.config(scrollregion=self.table_frame_canvas.bbox("all"))

    def create_table_header(self):
    
      headers = ("Title", "Author", "Rating")
    
    # Adjust width based on the window width
      window_width = self.winfo_width()
      if window_width >= 1366:  # Assumed threshold for fullscreen (or large window)
        header_width = 450
      else:
        header_width = 250

    # Dynamically adjust header font size based on window width
      header_font = ('Arial', int(window_width / 5000), 'bold')  # Adjust font size dynamically

      for idx, header in enumerate(headers):
        header_label = ctk.CTkLabel(self.table_frame, text=header, font=header_font, fg_color="#005D99", width=header_width, height=40, anchor="center", text_color="white", corner_radius=5)
        header_label.grid(row=0, column=idx, padx=5, pady=5, sticky="nsew")

    

    def create_table_row(self, row_idx, title, author, rating, row_font):
        """Create individual rows for the table."""
        title_label = ctk.CTkLabel(self.table_frame, text=title, font=row_font, fg_color="#2E3B56", anchor="center", text_color="white", corner_radius=5)
        title_label.grid(row=row_idx, column=0, padx=5, pady=5, sticky="nsew")
        title_label.bind("<Button-1>", lambda e, url=f"https://en.wikipedia.org/wiki/{title.replace(' ', '_')}": webbrowser.open(url))

        author_label = ctk.CTkLabel(self.table_frame, text=author, font=row_font, fg_color="#2E3B56", anchor="center", text_color="white", corner_radius=5)
        author_label.grid(row=row_idx, column=1, padx=5, pady=5, sticky="nsew")
        author_label.bind("<Button-1>", lambda e, url=f"https://en.wikipedia.org/wiki/{author.replace(' ', '_')}": webbrowser.open(url))

        rating_label = ctk.CTkLabel(self.table_frame, text=rating, font=row_font, fg_color="#2E3B56", anchor="center", text_color="white", corner_radius=5)
        rating_label.grid(row=row_idx, column=2, padx=5, pady=5, sticky="nsew")
        rating_label.bind("<Button-1>", lambda e, url=f"https://www.goodreads.com/search?q={title.replace(' ', '+')}+movie": webbrowser.open(url))


    def sort_books_command(self, option):
        """Sort the books based on the selected option."""
        if option == "ALL":
            self.books = self.db_interface.fetch_books()
        elif option == "TITLE(A-Z)":
            self.books = self.db_interface.sort_books(self.books, by="TITLE")
        elif option == "AUTHOR(A-Z)":
            self.books = self.db_interface.sort_books(self.books, by="AUTHOR")
        elif option == "RATINGS(1-5)":
            self.books = self.db_interface.sort_books(self.books, by="RATING")
        
        self.populate_table(self.books)

    def search_books(self, event):
        """Search books by title, author, or rating."""
        query = self.search_field.get().lower()
        filtered_books = self.db_interface.search_books(query)
        self.populate_table(filtered_books)

    def on_back_button_click(self):
        """Navigate back to the previous window (MenuWindow)."""
        if self.root_window:
            self.destroy()  # Close the current window
            self.root_window.deiconify()  # Show the root window (assuming it's hidden)


if __name__ == "__main__":
    viewWIN = ViewWindow(root_window=None)
    viewWIN.mainloop()
