import json

class booksColloection:

    def __init__(self):
        self.books_list = []
        self.storage_file = 'book_data.json'
        self.read_data()

    def read_data(self):
        try:
            with open(self.storage_file,"r") as file:
                self.books_list = json.load(file)

        except (FileNotFoundError,json.JSONDecodeError):
            self.books_list = []

    def save_data(self):
        with open(self.storage_file , "w") as file:
            json.dump(self.books_list, file, indent=4)
  
    def add_book(self):
        book_title = input("Enter the book title: ")
        book_author = input("Enter the book author: ")
        publication_year = input("Enter the publication year: ")

        book_read = input("Have you read this book? (yes/no): ").strip().lower() == "yes"

        new_book = {
            "title": book_title,
            "author": book_author,
            "publication_year": publication_year,
            "read": book_read
        }

        self.books_list.append(new_book)
        self.save_data()
        print( "New book added to the collection")

    while True:
        def start_app(self):
            print("welcome to the book collection app")
            print("1. Add a new book")
            print("2. Exit")
            choice = input("Enter your choice: 1 or 2")

            if choice == "1":
                self.add_book()

            elif choice == "2":
                print("thanks for using the app")
            
            else:
                print("Invalid choice, please try again")

            if __name__ == "__main__":
                bookmanager = booksColloection()
                bookmanager.start_app()