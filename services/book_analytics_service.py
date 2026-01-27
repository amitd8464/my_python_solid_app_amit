import numpy as np
from domain.book import Book
from collections import defaultdict

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
        counts = np.array([b.ratings_count for b in books])

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
        counts = np.array([b.ratings_count for b in books])
        prices = np.array([b.price_usd for b in books])

        scores = (ratings * np.log1p(counts)) / prices

        return {book.book_id: float(score) for book, score in zip(books, scores)}

    def median_price_by_genre(self, books: list[Book]) -> dict[str, float]:
        genres = {
            "Fanstasy": 0,
            "Sci-Fi": 1,
            "Non-Fiction": 2,
            "Mystery": 3,
            "Romance": 4,
            "Technology": 5,
            "History": 6
        }

        genre_prices = defaultdict(list)
        # array to hold per-genre median prices (initialized to zeros)
        for b in books:
            genre_prices[b.genre].append(b.price_usd)
       
        return {
            genre: f'${float(np.median(prices)):.2f}'
            for genre, prices in genre_prices.items()
        }