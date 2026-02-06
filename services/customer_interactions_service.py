from repositories.customer_interactions_repository_protocol import CustomerInteractionsRepositoryProtocol
from domain.customer_interaction import CustomerInteraction

class CustomerInteractionsService:
    def __init__(self, repo: CustomerInteractionsRepositoryProtocol):
        self.repo = repo
    
    def get_all_interactions(self) -> list[CustomerInteraction]:
        return self.repo.get_all_interactions()
