"""
Docstring for domain.customer_interaction

Interactions only include check in ("I") and check out ("O")
Tracks the book object of the interaction
This class will only be used from book repository to create new record of interaction
"""

from dataclasses import dataclass, field
from typing import Literal
import json
import uuid
from datetime import datetime
from enum import Enum


class InteractionType(Enum):
    IN = "I"
    OUT = "O"

@dataclass
class CustomerInteraction:
    # defining constants for interaction type
    book_id: str
    interaction: InteractionType
    interaction_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime = field(default_factory=datetime.now)

    def __post_init__(self):
        # ensuring that an accidental "I" passed through is converted to Enum
        if isinstance(self.interaction, str):
            self.interaction = InteractionType(self.interaction)
        
    def __str__(self) -> str:     
        interaction_type = "Check In" if self.interaction == InteractionType.IN else "Check Out"   
        res = (
            f"Timestamp:       {self.timestamp}\n"
            f"Interaction ID:  {self.interaction_id}\n"
            f"Book ID:         {self.book_id}\n"
            f"Action:       {interaction_type}\n"
        )  
        separator = "-" * 40
        return f"\n{res}\n{separator}\n"
    
    @classmethod
    def from_dict(cls, data:dict) -> 'CustomerInteraction':
        # Gemini explained that it is better to store datetime in isoformat()
        # in JSON files, and convert back when reading from the file
        if isinstance(data.get("timestamp"), str):
            data["timestamp"] = datetime.fromisoformat(data["timestamp"])
        return cls(**data)

    def to_dict(self) -> dict:
        return {
            "interaction_id": self.interaction_id,
            "book_id": self.book_id,
            "interaction": self.interaction.value,
            "timestamp": self.timestamp.isoformat()
        }
