### Programa principal ###
from fastapi import FastAPI
from endpoints import user
from auth import auth
from endpoints import expenses

app = FastAPI()

app.include_router(user.router)
app.include_router(auth.router)
app.include_router(expenses.router)

@app.get("/")
async def hi():
    return {"Bienvenidos":"Esta es una API de control de gastos"}

