### OPERACIONES CRUD PARA LOS GASTOS ###

from datetime import datetime, timedelta, date
from fastapi import Depends

#Día actual
today = date.today()

from db.client import db_expenses
from models.expenses import expenses
from schemas.expenses import expenses_schema,expense_schema
from auth.auth import current_user
from models.user import User


def create_expenses(expense: expenses, user: User):
    dict_spent = expense.dict()
    dict_spent.pop("id",None)

    dict_spent["user"] = user["username"]
    dict_spent["date"] = datetime.utcnow().date().isoformat()

    result = db_expenses.insert_one(dict_spent)

    new_spent = db_expenses.find_one({"_id":result.inserted_id})
    return expense_schema(new_spent)
#{
#  "title":"Super",
#  "amount":20,
#  "category":"food"
#}


async def get_expenses(user: User):
    user_expenses_cursor = db_expenses.find({"user": user["username"]})
    user_expenses = list(user_expenses_cursor)  # Convierte el cursor a lista
    return expenses_schema(user_expenses)

async def get_expenses_category(category: str, user: User):
    # Filtra directamente en la consulta a la base de datos
    user_expenses_cursor = db_expenses.find({"user": user["username"], "category": category})
    user_expenses = list(user_expenses_cursor)  # Convierte el cursor a lista
    return expenses_schema(user_expenses)
# pasar http://127.0.0.1:8000/expenses/food


def update_expenses():
    pass


def delete_expenses():
    pass