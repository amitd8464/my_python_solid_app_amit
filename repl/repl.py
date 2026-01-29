import requests
from services.book_generator_service import generate_books_json
from domain.book import Book
from services.book_service import BookService
from services.book_analytics_service import BookAnalyticsService
from repositories.book_repository import BookRepository
from pprint import pprint

class BookREPL:
    def __init__(self, book_svc, book_analytics_svc):
        self.running = True
        self.book_svc = book_svc
        self.book_analytics_svc = book_analytics_svc

    def start(self):
        print('Welcome to the book app! Type \'Help\' for a list of commands!')
        books = self.book_svc.get_all_books()
        pprint(self.book_analytics_svc.median_price_by_genre(books))
        while self.running:
            cmd = input('>>>').strip()
            self.handle_command(cmd)
    
    def handle_command(self, cmd):
        if cmd == 'exit':
            self.running = False
            print('Goodbye!')
        elif cmd == 'getAllRecords':
            self.get_all_records()
        elif cmd == 'addBook':
            self.add_book()
        elif cmd == 'deleteBook':
            self.delete_book()
        elif cmd == 'findByName':
            self.find_book_by_name()
        elif cmd == 'help':
            print('Available commands: addBook, getAllRecords, findByName, getAveragePrice, getTopBooks, help, exit')
        elif cmd == 'getJoke':
            self.get_joke()
        elif cmd == "getAveragePrice":
            self.get_average_price()
        elif cmd == "getTopBooks":
            self.get_top_books()
        elif cmd == "getValueScores":
            self.get_value_scores()
        elif cmd == "mostPopularGenre":
            self.most_popular_genre()
        else:
            print('Please use a valid command!')
    
    def most_popular_genre(self):
        books = self.book_svc.get_all_books()
        print(self.book_analytics_svc.most_popular_genre_by_year(books))
    def get_average_price(self):
        books = self.book_svc.get_all_books()
        print(self.book_analytics_svc.average_price(books))
    def get_top_books(self):
        books = self.book_svc.get_all_books()
        print(self.book_analytics_svc.top_rated(books))
    def get_value_scores(self):
        books = self.book_svc.get_all_books()
        print(self.book_analytics_svc.value_scores(books))

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
        print(books)

    def get_all_records(self):
        books = self.book_svc.get_all_books()
        print(books)

    def add_book(self):
        try:
            print('Enter Book Details:')
            title = input('Title: ')
            author = input('Author: ')
            book = Book(title= title, author=author)
            new_book_id = self.book_svc.add_book(book)
            print(new_book_id)
        except Exception as e:
            print(f'An unexpected error has occurred: {e}')
    def delete_book(self):
        try:
            book_id = input('Please enter the Book ID to delete: ')
            self.book_svc.delete_book(book_id)
            print(f'Book with ID {book_id} has been deleted.')
        except Exception as e:
            print(f'An unexpected error has occurred: {e}')
            
if __name__ == '__main__':
    generate_books_json()
    repo = BookRepository('books.json')
    book_service = BookService(repo)
    book_analytics_service = BookAnalyticsService()
    repl = BookREPL(book_service, book_analytics_service)
    repl.start()
