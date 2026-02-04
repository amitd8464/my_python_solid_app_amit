from domain.customer_interaction import CustomerInteraction
from domain.customer_interaction import InteractionType
from domain.book import Book
import json

class CustomerInteractionsRepository:
    def __init__(self, filepath):
        self.filepath = filepath
    
    def get_all_interactions(self) -> list[CustomerInteraction]:
        try:
            with open(self.filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return [CustomerInteraction.from_dict(item) for item in data]
        except FileNotFoundError:
            with open(self.filepath, 'w', encoding='utf-8') as f:
                json.dump([], f)
            return []

    def log_interaction(self, book_id: str, interaction: InteractionType):
        interactions = self.get_all_interactions()
        new_interaction = CustomerInteraction(book_id=book_id, interaction=interaction)
        interactions.append(new_interaction)
        with open(self.filepath, 'w', encoding='utf-8') as f:
            json.dump([i.to_dict() for i in interactions], f, indent=2)
