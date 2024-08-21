from fastapi import APIRouter,Depends
from bson import ObjectId
from fastapi import HTTPException

from crud.expenses import create_expenses,get_expenses,get_expenses_category,update_expenses
from models.expenses import expenses
from models.user import User
from auth.auth import current_user

router = APIRouter(prefix="/expenses")

@router.post("/", response_model=expenses)
async def create_spent(spent: expenses, user: User = Depends(current_user)):
    return create_expenses(spent, user)

@router.get("/", response_model=list[expenses])
async def get_spent(user: User = Depends(current_user)):
    return await get_expenses(user)  # Llama a la función y retorna el resultado

@router.get("/{category}", response_model=list[expenses])
async def get_spent_by_category(category: str, user: User = Depends(current_user)):
    return await get_expenses_category(category, user)

@router.put("/{id}")
async def update_spent(id,spent: expenses, user = Depends(current_user)):
    # Convertimos el id de la URL a ObjectId para la consulta
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid ID format")
    
    object_id = ObjectId(id)
    return update_expenses(object_id, spent, user)