from pymongo import MongoClient

db_client = MongoClient("mongodb://localhost:27017/")

db_users = db_client.expense_tracker.users

db_expenses = db_client.expense_tracker.expenses


# DB CATEGORY
db_category = db_client.expense_tracker.category

# Documentos a insertar
categories = [
    {"_id": "1", "nombre": "Groceries"},
    {"_id": "2", "nombre": "Leisure"},
    {"_id": "3", "nombre": "Electronics"},
    {"_id": "4", "nombre": "Utilities"},
    {"_id": "5", "nombre": "Clothing"},
    {"_id": "6", "nombre": "Health"},
    {"_id": "7", "nombre": "Others"}
]

    # Verifica si la colección está vacía
if db_category.count_documents({}) == 0:
    # Inserta los documentos en la colección
    db_category.insert_many(categories)
    print("Categorías insertadas con éxito")
else:
    print("La colección ya contiene datos")