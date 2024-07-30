from pymongo import MongoClient

db_client = MongoClient("mongodb://localhost:27017/")

db_users = db_client.expense_tracker.users

db_expenses = db_client.expense_tracker.expenses
