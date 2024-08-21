from crud.user import create_user,update_user,delete_user,get_all_users
from models.user import UserCreate,User,UserDeleteRequest
from fastapi import APIRouter, Depends

from models.user import User
from auth.auth import current_user


router = APIRouter(prefix="/users")


@router.post("/create", response_model=User)
async def create_users(user: UserCreate):
    return create_user(user)

@router.put("/update", response_model=User)
async def update_users(user: User, current_user: dict = Depends(current_user)):
    return update_user(user, current_user)

@router.delete("/delete", response_model=dict)
async def delete_users(user_delete_request: UserDeleteRequest, current_user: dict = Depends(current_user)):
    return await delete_user(user_delete_request, current_user)

@router.get("/", response_model=list[User])
async def read_users(user = Depends(current_user)):
    return get_all_users()