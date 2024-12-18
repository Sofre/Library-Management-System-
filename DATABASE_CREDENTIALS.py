class Database_CREDI:
    def __init__(self, filename="database.txt"):
        self.filename = "C:/Users/Duki/Desktop/DS&ALGO_PRJCT/database.txt"
        self.data = {}
        self.load_from_file()

    def load_from_file(self):
        
        try:
            with open(self.filename, "r") as file:
                for line in file:
                    email, password = line.strip().split(",")  
                    self.data[email] = password
        except FileNotFoundError:
            print(f"File '{self.filename}' not found. Starting with an empty database.")
        except Exception as e:
            print(f"Error reading from file: {e}")

    def save_to_file(self):
        
        with open(self.filename, "w") as file:
            for email, password in self.data.items():
                file.write(f"{email},{password}\n")

    def is_empty(self):
        if not self.data:
            print("Database is empty")
        else:
            print("Database is not empty")

    def insert(self, email, password):
    
        self.data[email] = password
        self.save_to_file()  

    def wipe(self):
     
        self.data.clear()
        self.save_to_file()  

    def print(self):
        if not self.data:
            print("No data to display.")
        else:
            for email, password in self.data.items():
                print(f"Email: {email}, Password: {password}")

    def check(self, email, password):
    
        if email in self.data and self.data[email] == password:
            return True
        return False




data = Database_CREDI()  


data.insert("data", "data")



data.print()

data.save_to_file()
