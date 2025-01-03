import sqlite3

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

    def check_if_book_exists(self, title):
        
        self.cursor.execute("SELECT * FROM books WHERE title = ?", (title,))
        book = self.cursor.fetchone()
        return book is not None

    def add_book(self, title, author, rating):
       
        if not self.check_if_book_exists(title):
            self.cursor.execute("INSERT INTO books (title, author, rating) VALUES (?, ?, ?)",
                                (title, author, rating))
            self.conn.commit()
        else:
            raise ValueError("This book already exists in the database.")

    def fetch_books(self):
       
        self.cursor.execute("SELECT title, author, rating FROM books")
        rows = self.cursor.fetchall()
        books = [{"title": row[0], "author": row[1], "rating": row[2]} for row in rows]
        return books

    def search_books(self, query):
        query = f"%{query}%"
        self.cursor.execute("SELECT id, title, author, rating, available FROM books WHERE title LIKE ? OR author LIKE ?", (query, query))
        rows = self.cursor.fetchall()

      
        books = [{
            "id": row[0],
            "title": row[1],
            "author": row[2],
            "rating": row[3],
            "available": row[4]
        } for row in rows]

        return books

    def sort_books(self, books, by="title"):
        
        if by == "TITLE":
            books.sort(key=lambda x: x["title"])
        elif by == "AUTHOR":
            books.sort(key=lambda x: x["author"])
        elif by == "RATING":
            books.sort(key=lambda x: float(x["rating"]))  
        return books
    
    def issue_book(self, book_id):
    
        try:
           self.cursor.execute("UPDATE books SET available = 0 WHERE id = ?", (book_id,))
           self.conn.commit()  
           print(f"Book with ID {book_id} has been marked as issued.")
        except sqlite3.Error as e:
           print(f"Error while issuing the book: {e}")
           self.conn.rollback()  

        

    def return_book(self, book_id):
     
        self.cursor.execute("UPDATE books SET available = 1 WHERE id = ?", (book_id,))
        self.conn.commit()
    

    def close(self):
        
        self.conn.close()
