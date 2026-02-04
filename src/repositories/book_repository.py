import json
from domain.book import Book
from repositories.book_repository_protocol import BookRepositoryProtocol
from repositories.customer_interactions_repository import CustomerInteractionsRepository
from custom_errors.book_not_found import BookNotFoundError
from domain.customer_interaction import InteractionType

class   BookRepository(BookRepositoryProtocol):
    def __init__(self, customer_interactions_repo: CustomerInteractionsRepository, filepath: str="books.json"):
        self.filepath = filepath
        self.ci_repo = customer_interactions_repo

    def get_all_books(self) -> list[Book]:
        with open(self.filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return [Book.from_dict(item) for item in data]

    def add_book(self, book:Book) -> str:
        books = self.get_all_books()
        books.append(book)
        with open(self.filepath, 'w', encoding='utf-8') as f:
            json.dump([b.to_dict() for b in books], f, indent=2)
        return book.book_id

    def delete_book(self, book_id: str):
        books = self.get_all_books()
        books = [b for b in books if b.book_id != book_id]
        with open(self.filepath, 'w', encoding='utf-8') as f:
            json.dump([b.to_dict() for b in books], f, indent=2)

    def find_book_by_name(self, query: str) -> Book:
        return [b for b in self.get_all_books() if b.title == query]
    
    def find_book_by_id(self, book_id: str) -> Book:
        books = self.get_all_books()
        return next((b for b in books if b.book_id == book_id), None)

    def check_out_book(self, title: str, author: str) -> Book:
        books = self.get_all_books()
        book =  next((b for b in books if b.title == title and b.author == author), None)
        if not book:
            raise BookNotFoundError("Sorry, this book does not exist.")
        else:
            # handle check out and JSON persistence
            book.check_out()
            books = [b for b in books if b.book_id != book.book_id]
            books.append(book)

            with open(self.filepath, 'w', encoding='utf-8') as f:
                json.dump([b.to_dict() for b in books], f, indent=2)

            # call method from ci repo to handle interaction persistence
            self.ci_repo.log_interaction(book_id=book.book_id, interaction=InteractionType.OUT)
            return book
    def check_in_book(self, book_id: str):
        books = self.get_all_books()
        book = next((b for b in books if b.book_id == book_id), None)

        if not book:
            raise BookNotFoundError("Sorry, this book does not exist.")
        else:
            book.check_in() # will raise BookAlreadyAvailableError if book.available=true
            books = [b for b in books if b.book_id != book.book_id]
            books.append(book)

            with open(self.filepath, 'w', encoding='utf-8') as f:
                json.dump([b.to_dict() for b in books], f, indent=2)
            
            # call method from ci repo to handle interaction persistence
            self.ci_repo.log_interaction(book_id=book.book_id, interaction=InteractionType.IN)
