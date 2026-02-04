from typing import Optional
from datetime import datetime
from pydantic import BaseModel
from uuid import UUID
from src.domain.customer_interaction import InteractionType

class CustomerInteractionCreate(BaseModel):
    interaction: InteractionType
    book_id: UUID

class CustomerInteractionRead(CustomerInteractionCreate):
    interaction_id: UUID
    timestamp: datetime