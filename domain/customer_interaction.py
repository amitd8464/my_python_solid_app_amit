"""
Docstring for domain.customer_interaction

Interactions only include check in ("I") and check out ("O")
Tracks the book object of the interaction
This class will only be used from book repository to create new record of interaction
"""

from book import Book

class CustomerInteraction:
    def __init__(self, book: Book, interaction: str):
        allowed_interactions = ["I", "O"]
        self.book = book
        if interaction not in allowed_interactions:
            raise ValueError(
                f"Status must be either 'I' for check in or 'O' for check out\nInstead received {interaction}"
            )
        self.interaction = interaction
    
    #def log_interaction()