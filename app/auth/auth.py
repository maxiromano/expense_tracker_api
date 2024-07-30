from fastapi import APIRouter,Depends,status,HTTPException
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from jose import jwt,JWTError
from passlib.context import CryptContext

from datetime import datetime,timedelta
import os

from db.client import db_users
from models.user import User,UserCreate
from schemas.user import user_schema


# Algoritmo de hash
ALGORITHM = "HS256"
ACCESS_TOKEN_DURATION = 60
SECRET = os.getenv("SECRET")

oauth2 = OAuth2PasswordBearer(tokenUrl="/login")

crypt = CryptContext(schemes=["bcrypt"])

router = APIRouter()


# SEARCH
async def search_user(field: str, key: str):
    try:
        user = db_users.find_one({field: key})
        if user:
            return user
    except Exception as e:
        print(f"Error: {e}")
        return None


# Auntenticar usuario
async def autenticate_user(token:str= Depends(oauth2)):
    exception = HTTPException(status_code=401, detail="Credenciales invalidas")
    try:
        username = jwt.decode(token,SECRET,algorithms=[ALGORITHM]).get("sub")
        if username is None:
            raise exception
    except JWTError:
        raise exception
    
    return await search_user("username",username)

async def current_user(user: User = Depends(autenticate_user)):
    return user

@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_dict = await search_user("username", form.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="El usuario no es correcto")
    
    if not crypt.verify(form.password, user_dict["password"]):
        raise HTTPException(status_code=400, detail="La contraseña no es correcta")
    
    access_token_expiration = timedelta(minutes=ACCESS_TOKEN_DURATION)
    expire = datetime.utcnow() + access_token_expiration

    access_token = {"sub": user_dict["username"], "exp": expire}

    return {"access_token": jwt.encode(access_token, SECRET, algorithm=ALGORITHM), "token_type": "bearer"}
# body -> form (username,password)


@router.get("/users/me")
async def me(user:User = Depends(current_user)):  
    return user_schema(user)

# con el token generado previamente en /login si le pasamos ese access_token a http://127.0.0.1:8000/users/me obtenemos el usuario