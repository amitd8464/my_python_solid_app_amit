import numpy as np
from domain.book import Book

# Ground rules for NumPy:
#   1. Keep NumPy only the service layer!
#       --> ndarrays remain in this service -- they should not leave the service layer!
#

class BookAnalyticsService:
    def average_price(self, books: list[Book]):
        prices = np.array([b.price_usd for b in books])
        return float(prices.mean())
    def top_rated(self, books: list[Book], min_ratings: int = 1000, limit: int = 10):
        
        # ratings and counts for ALL books
        ratings = np.array([b.average_rating for b in books])
        counts = np.array([b.ratings_count for b in  books])

        # Creating a mask to filter our ratings and books according to min_ratings
        mask = counts >= min_ratings
       
        # here, we use the mask to have an array of books and of ratings where count >= min_ratings
        filtered_books = np.array(books)[mask]
        scores = ratings[mask]

        sorted_idx = np.argsort(scores)[::-1]
        return filtered_books[sorted_idx].tolist()[:limit]

# value score = rating * log(ratings_count) / price

    def value_scores(self, books: list[Book]) -> dict[str, float]:
        ratings = np.array([b.average_rating for b in books])
        counts = np.array([b.ratings_count for b in  books])
        prices = np.array([b.price_usd for b in books])

        scores = (ratings * np.log1p(counts)) / prices
        
        return {
            book.book_id: float(score)
            for book, score in zip(books, scores)
        }