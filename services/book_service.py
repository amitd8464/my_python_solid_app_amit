from repositories.book_repository_protocol import BookRepositoryProtocol
from domain.book import Book

class BookService:
    def __init__(self, repo: BookRepositoryProtocol):
        self.repo = repo

    def get_all_books(self) -> list[Book]:
        return self.repo.get_all_books()

    def add_book(self, book:Book) -> str:
        return self.repo.add_book(book)

    def delete_book(self, book_id: str):
        self.repo.delete_book(book_id)

    def find_book_by_name(self, query:str) -> list[Book]:
        if not isinstance(query, str):
            raise TypeError("Query must be a string")
        return self.repo.find_book_by_name(query)
    
    def update_book_details(self, book_id: str, updates: dict) -> Book:
        # Prevent primary key (book_id) from being updated
        if "book_id" in updates:
            del updates["book_id"] 
        
        return self.repo.update_book(book_id, updates)
    
    def check_out_book(self, title: str, author: str):
        
        return self.repo.check_out_book(title, author)

    def check_in_book(self, book_id: str):
        return self.repo.check_in_book(book_id)