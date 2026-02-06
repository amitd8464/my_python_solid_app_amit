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

    def __str__(self) -> str:
        status = "◌ Available" if self.available else " ● Checked Out"
        
        # Main information about the book prints first
        primary = (
            f"Title:        {self.title}\n"
            f"Author:       {self.author}\n"
            f"Status:       {status}\n"
            f"Book ID:      {self.book_id}"
        )
        
        # Secondary information will print here, separated by a line
        secondary = (
            f"Price:        ${self.price_usd:.2f}\n"
            f"Year:         {self.publication_year or 'Unknown'}\n"
            f"Rating:       {self.average_rating or 'No ratings'} ({self.ratings_count or 0} reviews)\n"
            f"Publisher:    {self.publisher or 'N/A'}\n"
            f"Format:       {self.format or 'N/A'} ({self.language or 'Unknown'})"
        )
        
        separator = "-" * 40
        return f"\n{primary}\n{separator}\n{secondary}\n"
    
    def quick_info(self) -> str:
        status = "◌ Available" if self.available else " ● Checked Out"
        quick_info = (
            f"Title:        {self.title}\n"
            f"Author:       {self.author}\n"
            f"Price:       {status}\n"
            f"Book ID:      {self.book_id}"
        )
        return f"\n{quick_info}\n"

    def check_out(self) -> bool:
        if not self.available:
            raise BookUnavailableError('Sorry! This book is already checked out.')
        self.available = False
    
    def check_in(self) -> bool:
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