### Operaciones para crear, modificar y eliminar usuarios ###
from fastapi import HTTPException
from auth.auth import crypt
from models.user import User,UserCreate
from schemas.user import user_schema
from db.client import db_users

# Función para hashear una contraseña
def hash_password(password: str) -> str:
    return crypt.hash(password)


def create_user(user: UserCreate):
    user_dict = user.dict()
    user_dict["password"] = hash_password(user.password)
    
    try:
        result = db_users.insert_one(user_dict)
        new_user = db_users.find_one({"_id": result.inserted_id})
        return user_schema(new_user)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")
# {
#  "username":"camion",
#  "email":"camion3@gmial.com",
#  "password":1234
# }


def update_user(user: User):
    user_dict = user.dict()
    user_dict.pop("id",None)
    try:
        result = db_users.find_one_and_replace({"email":user.email},user_dict)
        if result is None:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        return user_schema(result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")

# {
#  "username":"carlos",
#  "email":"carlos2@gmial.com"
# }


def delete_user(user: User):
    found = db_users.delete_one({"email":user.email})
    if not found:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return {"detail": "Usuario eliminado correctamente"}

#{
#  "username":"milanesa",
#  "email":"milanesa3@gmial.com"
#}

def get_all_users():
    users = db_users.find()
    return [user_schema(user) for user in users]
