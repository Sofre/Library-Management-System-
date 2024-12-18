#LMS_LIB_ADD
import customtkinter as ctk
import requests
from DATABASEBK_INTERFACE import DatabaseInterface
from tkinter import messagebox
from PIL import Image, ImageTk

class AddBookWindow(ctk.CTk):
    def __init__(self, root_window=None, **kwargs):
        super().__init__(**kwargs)
        self.geometry('800x600')
        self.title("Add Book")
        ctk.set_appearance_mode("dark")
        png_image = Image.open("D:/LMS/Library-Management-System-/IMG/online-library.png")


        png_image.save('D:/LMS/Library-Management-System-/IMG/online-library.ico', format='ICO')


        self.iconbitmap('D:\LMS\Library-Management-System-\IMG\online-library.ico')

        self.label = ctk.CTkLabel(self, text="Library Managment Adding Book", font=("Arial", 30), text_color="grey")
        self.label.place(relx=0.5, rely=0.1, anchor="center")

        self.db_interface = DatabaseInterface()

        # UI Element for adding a book (only title)
        self.title_entry = ctk.CTkEntry(self, placeholder_text="Book Title", width=250)
        self.title_entry.place(relx=0.5, rely=0.3, anchor="center")

        # Add Book button
        self.add_button = ctk.CTkButton(self, text="Add Book", command=self.add_book, width=120)
        self.add_button.place(relx=0.5, rely=0.6, anchor="center")

        # Back button to return to previous window
        self.back_button = ctk.CTkButton(self, text="Cancel", command=self.on_back_button_click, width=120, fg_color="#E52B50", hover_color="#C41E3A")
        self.back_button.place(relx=0.5, rely=0.7, anchor="center")

        self.author_label = ctk.CTkLabel(self, text="© 2024, Developed by инг. Душко Софрониевски", font=("Arial", 12), text_color="gray")
        self.author_label.place(relx=0.5, rely=0.98, anchor="center")

        self.root_window = root_window

    def add_book(self):
        try:
            title = self.title_entry.get().strip()

            # Validate input
            if not title:
                raise ValueError("The book title must be filled out.")

            # Check if the book exists in the database
            if self.db_interface.check_if_book_exists(title):
                raise ValueError("This book already exists in the database.")

            # Fetch the book details (author and rating) from the web if the book is not in the database
            book_data = self.fetch_book_details_from_web(title)

            if book_data:
                author = book_data.get('author', 'Unknown Author')  # Fallback to 'Unknown Author'
                rating = book_data.get('rating', 0)  # Fallback to 'N/A' if no rating is available

                # Add the book to the database
                self.db_interface.add_book(title, author, rating)

                # Success message
                messagebox.showinfo("Success", "Book added successfully!")

                # Clear the entries
                self.clear_entries()
            else:
                messagebox.showerror("Error", "Book details not found.")

        except ValueError as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")

    def fetch_book_details_from_web(self, title):
        """Fetch the book details (author and rating) from a public API (Google Books API)."""
        try:
            # Google Books API query
            url = f"https://www.googleapis.com/books/v1/volumes?q={title}"

            # Send the request
            response = requests.get(url)
            response.raise_for_status()  # Raise error for bad responses

            # Parse the JSON response
            data = response.json()

            if 'items' not in data:
                raise ValueError("Book not found.")

            # Extract details from the first result
            book_info = data['items'][0]['volumeInfo']
            author = book_info.get('authors', ['Unknown Author'])[0]
            rating = book_info.get('averageRating', None)

            # Convert rating to a proper format (1.0 to 5.0)
            if rating is not None:
                rating = round(rating, 1)  # Round the rating to one decimal place
            else:
                rating = 0  # If no rating is available

            return {'author': author, 'rating': rating}

        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", f"Failed to fetch data from the web: {e}")
            return None

    def clear_entries(self):
        """Clear all the input fields."""
        self.title_entry.delete(0, ctk.END)

    def on_back_button_click(self):
        """Navigate back to the previous window (MenuWindow)."""
        if self.root_window:
            self.destroy()  # Close the current window
            self.root_window.deiconify()  # Show the root window (assuming it's hidden)


if __name__ == "__main__":
    add = AddBookWindow()  # This initializes the MenuWindow
    add.mainloop()  # This starts the tkinter main loop, displaying the menu window