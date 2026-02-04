import numpy as np
from domain.book import Book
from collections import defaultdict
import pandas as pd

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

    # Used NumPy for this method
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
    
    def most_popular_genre_by_year(self, books: list[Book], year=2025):
        df = pd.DataFrame(books)

        genre_sales = df.groupby("genre").count().sort_values(by="title", ascending=False)
        most_popular = genre_sales.index[0]
        return most_popular

    def top_rated_with_pandas(self, books: list, min_ratings: int = 1000, limit: int = 10) -> list:
        df = pd.DataFrame([{
            'book': b,
            'avg': b.average_rating,
            'count': b.ratings_count
        } for b in books])
        filtered = df[df['count'] >= min_ratings].sort_values('avg', ascending=False)
        return filtered['book'].tolist()[:limit]

    def value_scores_with_pandas(self, books: list, limit: int = 10) -> dict[str, float]:
        df = pd.DataFrame([{
            'book_id': b.book_id,
            'avg': b.average_rating,
            'count': b.ratings_count,
            'price': b.price_usd
        } for b in books])
        df['score'] = df['avg'] * np.log1p(df['count']) / df['price']
        # set_index() sets book_id as the index
        # we do this because we want to end up with a dict[str, float]
        # where book_id is the key and the value score is the float
        # sometimes numpy works with float64, but we need to return float,
        # hence the defensive use of .astype()
        return (
            df
            .sort_values('score', ascending=False)
            .head(limit)
            .set_index('book_id')['score']
            .astype(float).to_dict()
        ) 