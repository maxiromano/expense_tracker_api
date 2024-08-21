### Operaciones para crear, modificar y eliminar usuarios ###
from fastapi import HTTPException
from auth.auth import crypt
from models.user import User,UserCreate,UserDeleteRequest
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
#  "password":"1234
# }


def update_user(user: User, current_user: dict):
    # Convertir current_user de dict a User
    if isinstance(current_user, dict):
        current_user = User(**current_user)
    
    if not isinstance(user, User):
        raise HTTPException(status_code=400, detail="Datos de usuario inválidos")
    
    if not isinstance(current_user, User):
        raise HTTPException(status_code=400, detail="Datos del usuario actual inválidos")
    
    if user.email != current_user.email:
        raise HTTPException(status_code=403, detail="No tienes permiso para modificar este usuario")
    
    # Obtener el usuario actual de la base de datos para mantener la contraseña
    existing_user = db_users.find_one({"email": current_user.email})
    if existing_user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    # Crear un diccionario para actualizar sin la contraseña
    update_data = user.dict(exclude={"id"})
    
    # Mantener la contraseña del usuario existente
    update_data["password"] = existing_user.get("password")

    try:
        result = db_users.find_one_and_update({"email": user.email}, {"$set": update_data}, return_document=True)
        if result is None:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        
        updated_user_dict = user_schema(result)
        return User(**updated_user_dict)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")
# {
#  "username":"carlos",
#  "email":"carlos2@gmial.com"
# }


async def delete_user(user_delete_request: UserDeleteRequest, current_user: dict):
    if current_user is None:
        raise HTTPException(status_code=401, detail="Usuario no autenticado")
    
    # Convertir current_user de dict a User si es necesario
    if isinstance(current_user, dict):
        current_user = User(**current_user)
    
    # Verificar permisos
    if user_delete_request.email != current_user.email:
        raise HTTPException(status_code=403, detail="No tienes permiso para eliminar este usuario")

    # Intentar eliminar el usuario
    result = db_users.delete_one({"email": user_delete_request.email})
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    return {"detail": "Usuario eliminado correctamente"}
#{
#  "email":"milanesa3@gmial.com"
#}


def get_all_users():
    users = db_users.find()
    return [user_schema(user) for user in users]
