from typing import Protocol
from domain.customer_interaction import CustomerInteraction
from domain.customer_interaction import InteractionType

class CustomerInteractionsRepositoryProtocol(Protocol):
    
    def get_all_interactions(self) -> list[CustomerInteraction]:
        ...
    def log_interaction(self, book_id: str, interaction: InteractionType):
        ...