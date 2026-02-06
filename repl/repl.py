import requests
from services.book_generator_service_V2 import generate_books_json
from services.book_generator_bad_data_service import generate_books
from domain.book import Book
from services.book_service import BookService
from services.customer_interactions_service import CustomerInteractionsService
from dataclasses import fields
from services.book_analytics_service import BookAnalyticsService
from repositories.book_repository import BookRepository
from repositories.customer_interactions_repository import CustomerInteractionsRepository
from custom_errors.book_not_found import BookNotFoundError
from pprint import pprint

class BookREPL:
    def __init__(self, book_svc, book_analytics_svc, customer_interactions_svc):
        self.running = True
        self.book_svc = book_svc
        self.book_analytics_svc = book_analytics_svc
        self.customer_interactions_svc = customer_interactions_svc

    def start(self):
        print('Welcome to the book app! Type \'Help\' for a list of commands!')
        books = self.book_svc.get_all_books()
        while self.running:
            print()
            cmd = input('>>>').strip()
            self.handle_command(cmd)
    
    def handle_command(self, cmd):
        match cmd:
            case 'exit':
                self.running = False
                print('Goodbye!')
            case 'getAllRecords':
                self.get_all_records()
            case 'addBook':
                self.add_book()
            case 'deleteBook':
                self.delete_book()
            case 'findByName':
                self.find_book_by_name()
            case 'updateBook':
                self.update_book()
            case 'help':
                print('Available commands: addBook, deleteBook, checkIn, checkOut, listInteractions, getAllRecords, findByName, getAveragePrice, getTopBooks, help, exit')
            case 'getJoke':
                self.get_joke()
            case 'getAveragePrice':
                self.get_average_price()
            case 'getTopBooks':
                self.get_top_books()
            case 'getValueScores':
                self.get_value_scores()
            case 'mostPopularGenre':
                self.most_popular_genre()
            case 'checkOut':
                self.check_out()
            case 'checkIn':
                self.check_in()
            case 'listInteractions':
                self.list_interactions()
            case _:
                print('Please use a valid command!')
    
    def list_interactions(self):
        interactions = self.customer_interactions_svc.get_all_interactions()
        for i in interactions:
            print(i)

    # check in / check out methods:

    def check_out(self):
        title = input("Enter the book title: ")
        author = input("Enter the book author: ")
        
        try:
            book = self.book_svc.check_out_book(title, author)
            print(f'Success! You have checked out the following book:\nTitle: {book.title}\nAuthor: {book.author}\nBook ID: {book.book_id}')
        except Exception as e:
            print(e)
    
    def check_in(self):
        book_id = input("Please enter the book ID: ")
        
        try:
            self.book_svc.check_in_book(book_id)
            print('Your book has been successfully checked in!')
        except Exception as e:
            print(e)
    
    def most_popular_genre(self):
        books = self.book_svc.get_all_books()
        print(f'The most popular genre at the moment is {self.book_analytics_svc.most_popular_genre_by_year(books)}')
    def get_average_price(self):
        books = self.book_svc.get_all_books()
        print(f'Average Book Price: ${self.book_analytics_svc.average_price(books)}')
    def get_top_books(self):
        books = self.book_svc.get_all_books()
        top_books = self.book_analytics_svc.top_rated(books)
        print("Top 10 Book Titles:")
        i = 1
        for b in top_books:
            print(f'{i}. {b.title}')
            i+=1
    def get_value_scores(self):
        books = self.book_svc.get_all_books()
        value_scores = self.book_analytics_svc.value_scores(books)
        for b_id, v in value_scores.items():
            print(f'ID {b_id}:      Score: {v}')

    def get_joke(self):
        try:
            url = "https://api.chucknorris.io/jokes/random"
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            print(response.json().get('value'))
        except requests.exceptions.Timeout:
            print("Request timed out.")
        except requests.exceptions.HTTPError as e:
            print(f"Something went wrong: {e}.")
        except requests.exceptions.RequestException as e:
            print(f"Something else went wrong: {e}.")
    
    def find_book_by_name(self):
        query = input('Please enter book name: ')
        books = self.book_svc.find_book_by_name(query)
        for b in books:
            print(b)

    def get_all_records(self):
        books = self.book_svc.get_all_books()
        for b in books:
            print(b.quick_info())

    def add_book(self):
        try:
            print('Enter Book Details:')
            title = input('Title: ')
            author = input('Author: ')
            book = Book(title= title, author=author)
            new_book_id = self.book_svc.add_book(book)
            print("\nYour book has been added!")
            print(f'ID: {new_book_id}')
        except Exception as e:
            print(f'An unexpected error has occurred: {e}')
    def delete_book(self):
        try:
            book_id = input('Please enter the Book ID to delete: ')
            self.book_svc.delete_book(book_id)
            print(f'\nBook with ID {book_id} has been deleted.')
        except Exception as e:
            print(f'An unexpected error has occurred: {e}')
    
    def update_book(self):
        updates = {}
        book_id = input("Please enter the book ID of the book you'd like to update:\n")
        print("\nWhich field would you like to update?\n")
        for f in ["1. Title", "2. Author", "3. Average Rating", "4. Price", "5. Publisher"]:
            print(f)
        print("")
        option = input("\nPlease input the number: ")
        match option:
            case "1":
                value = input("\nPlease enter the new title: ")
                updates["title"] = value
            case "2":
                value = input("\nPlease enter the new author: ")
                updates["author"] = value
            case "3":
                value = input("\nPlease enter the new rating: ")
                updates["average_rating"] = value
            case "4":
                value = input("\nPlease enter the new price: ")
                updates["price_usd"] = value
            case "5":
                value = input("\nPlease enter the new publisher: ")
                updates["publisher"] = value
            case _:
                print("Invalid option.")
                return

        updated_book = self.book_svc.update_book_details(book_id, updates)
        print("The book has been updated!")
        print(updated_book)
if __name__ == '__main__':
    generate_books_json()
    generate_books()
    # customer interactions repo will handle persistence of records for each check in and check out
    customer_interactions_repo = CustomerInteractionsRepository('customer_records.json')
    book_repo = BookRepository(customer_interactions_repo, 'books.json')
    book_service = BookService(book_repo)
    customer_interactions_service = CustomerInteractionsService(customer_interactions_repo)
    book_analytics_service = BookAnalyticsService()
    repl = BookREPL(book_service, book_analytics_service, customer_interactions_service)
    repl.start()
