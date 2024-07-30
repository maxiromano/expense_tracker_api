### Crear modelo para los gastos ###
from pydantic import BaseModel
from typing import Optional

class expenses(BaseModel):
    id:Optional[str] = None
    title:str
    amount:float
    id_users:str
    id_category:str
 