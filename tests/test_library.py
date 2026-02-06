import pytest
from unittest.mock import MagicMock
from domain.book import Book
from domain.customer_interaction import CustomerInteraction, InteractionType
from services.book_service import BookService
from custom_errors.book_unavailable import BookUnavailableError
from custom_errors.book_already_available import BookAlreadyAvailableError

@pytest.fixture
def sample_book():
    return Book(
        title="The Great Gatsby",
        author="F. Scott Fitzgerald",
        available=True,
        price_usd=15.99
    )

@pytest.fixture
def mock_repo():
    return MagicMock()

@pytest.fixture
def book_service(mock_repo):
    return BookService(repo=mock_repo)

def test_book_check_out_success(sample_book):
    sample_book.check_out()
    assert sample_book.available is False

def test_book_check_out_fail_already_checked_out(sample_book):
    sample_book.available = False
    with pytest.raises(BookUnavailableError):
        sample_book.check_out()

def test_book_check_in_success(sample_book):
    sample_book.available = False
    sample_book.check_in()
    assert sample_book.available is True

def test_interaction_enum_conversion():
    interaction = CustomerInteraction(book_id="123", interaction="I")
    assert interaction.interaction == InteractionType.IN

def test_service_find_book_by_name_success(book_service, mock_repo, sample_book):
    mock_repo.find_book_by_name.return_value = [sample_book]
    
    results = book_service.find_book_by_name("Gatsby")
    
    assert len(results) == 1
    assert results[0].title == "The Great Gatsby"
    mock_repo.find_book_by_name.assert_called_once_with("Gatsby")

def test_service_find_book_by_name_wrong_type(book_service):
    with pytest.raises(TypeError, match="Query must be a string"):
        book_service.find_book_by_name(123)

def test_service_check_out_calls_repo(book_service, mock_repo, sample_book):
    mock_repo.check_out_book.return_value = sample_book
    
    result = book_service.check_out_book("Gatsby", "Fitzgerald")
    
    assert result.title == "The Great Gatsby"
    mock_repo.check_out_book.assert_called_with("Gatsby", "Fitzgerald")

def test_service_delete_book(book_service, mock_repo):
    book_service.delete_book("uuid-123")
    mock_repo.delete_book.assert_called_once_with("uuid-123")


def test_book_to_dict(sample_book):
    data = sample_book.to_dict()
    assert data["title"] == "The Great Gatsby"
    assert data["available"] is True
    assert "book_id" in data

def test_book_from_dict():
    data = {
        "title": "1984",
        "author": "George Orwell",
        "available": True,
        "price_usd": 12.50
    }
    book = Book.from_dict(data)
    assert book.title == "1984"
    assert book.author == "George Orwell"

def test_book_str_output(sample_book):
    output = str(sample_book)
    assert "The Great Gatsby" in output
    assert "Available" in output

def test_customer_interaction_to_dict():
    interaction = CustomerInteraction(book_id="123", interaction=InteractionType.OUT)
    data = interaction.to_dict()
    assert data["interaction"] == "O"
    assert "timestamp" in data

def test_service_add_book(book_service, mock_repo, sample_book):
    mock_repo.add_book.return_value = "new-uuid"
    result = book_service.add_book(sample_book)
    assert result == "new-uuid"
    mock_repo.add_book.assert_called_once()

def test_service_check_in_calls_repo(book_service, mock_repo):
    book_service.check_in_book("uuid-123")
    mock_repo.check_in_book.assert_called_with("uuid-123")