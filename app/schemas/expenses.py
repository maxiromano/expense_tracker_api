### Crear esquema para gastos ###
from datetime import date

def expense_schema(spent):
    return {
        "id":str(spent["_id"]), 
        "title":spent["title"],
        "amount":spent["amount"],
        "date":spent["date"],
        "user":spent["user"],
        "category":spent["category"]
    }

def expenses_schema(expenses):
    return [expense_schema(expense) for expense in expenses]