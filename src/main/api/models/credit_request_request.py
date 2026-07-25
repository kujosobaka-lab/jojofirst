from src.main.api.models.base_model import BaseModel
from typing import Annotated
from src.main.api.generators.creation_rule import CreationRule

class CreditRequestRequest(BaseModel):
    accountId: int
    amount: Annotated[float, CreationRule(value_range=(5000, 15000))]
    termMonths: Annotated[int, CreationRule(value_range=(1, 12))]
