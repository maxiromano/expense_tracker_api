### Programa principal ###
from fastapi import FastAPI
from endpoints import user
from auth import auth

app = FastAPI()

app.include_router(user.router)
app.include_router(auth.router)

@app.get("/")
async def hi():
    return {"Bienvenidos":"Esta es una API de control de gastos"}

