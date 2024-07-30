### Crear modelo para los gastos ###
from pydantic import BaseModel
from typing import Optional
from datetime import date

class expenses(BaseModel):
    id: Optional[str] = None
    title: str
    amount: float
    date: Optional[str] = None
    user: Optional[str] = None
    category: str
 