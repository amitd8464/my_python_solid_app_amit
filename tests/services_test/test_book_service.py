import pytest

import services.book_service as book_service
from tests.mocks.mock_book_repository import MockBookRepo
from domain.book import Book

def test_get_all_books_positive():
    repo = MockBookRepo()
    svc = book_service.BookService(repo)
    books = svc.get_all_books()
    assert len(books) == 1

def test_find_book_name_negative():
    name = 3
    repo = MockBookRepo()
    svc = book_service.BookService(repo)

    with pytest.raises(TypeError) as e:
        book = svc.find_book_by_name(name)
    assert str(e.value) == "Query must be a string"

# We can build a positive and negative test for delete_book

def test_delete_book_positive():
    repo = MockBookRepo()
    svc = book_service.BookService(repo)

    book = Book(title="test", author="test") # pretty sure this should be a mock
    added_book_id = svc.add_book(book)
    svc.delete_book(added_book_id)

    books = svc.get_all_books()

    assert all([b.book_id != added_book_id for b in books])