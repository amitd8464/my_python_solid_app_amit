from dataclasses import dataclass, field
from typing import Optional
import uuid
from custom_errors.book_unavailable import BookUnavailableError
from custom_errors.book_already_available import BookAlreadyAvailableError

@dataclass
class Book:
    title: str
    author: str
    genre: Optional[int] = None
    publication_year: Optional[int] = None
    page_count: Optional[int] = None
    average_rating: Optional[float] = None
    ratings_count: Optional[int] = None
    price_usd: Optional[float] = None
    publisher: Optional[str] = None
    language: Optional[str] = None
    format: Optional[str] = None
    in_print: Optional[bool] = None
    sales_millions: Optional[float] = None
    last_checkout: Optional[str] = None
    available: Optional[bool] = None
    book_id: str = field(default_factory=lambda: str(uuid.uuid4()))

    '''
    for interview practice: this is a form of encapsulation
        even though book.available is a public variable, we are using mutator
        methods to change its value and apply additional checking logic

        Best practice would be to make most of these variables private and write
        getters and setters for them
    '''
    def check_out(self):
        if not self.available:
            raise BookUnavailableError('Sorry! This book is already checked out.')
        self.available = False
    
    def check_in(self):
        if self.available:
            raise BookAlreadyAvailableError('Book is already available.')
        self.available = True

    @classmethod
    def from_dict(cls, data:dict) -> 'Book':
        return cls(**data)

    def to_dict(self) -> dict:
        return {
            "book_id":self.book_id,
            "title": self.title,
            "author": self.author,
            "genre": self.genre,
            "publication_year": self.publication_year,
            "page_count": self.page_count,
            "average_rating": self.average_rating,
            "ratings_count": self.ratings_count,
            "price_usd": self.price_usd,
            "publisher": self.publisher,
            "language": self.language,
            "format": self.format,
            "in_print": self.in_print,
            "sales_millions": self.sales_millions,
            "last_checkout": self.last_checkout,
            "available": self.available
        }

'''
We could have a record that holds either check in or check out info

Attributes would be something like:
    book: Book
    type_of_check : check in or check out
    time : datetime of check in or check out

One object for check in: 
'''