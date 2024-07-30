from crud.user import create_user,update_user,delete_user,get_all_users
from models.user import UserCreate,User
from fastapi import APIRouter

router = APIRouter(prefix="/users")


@router.post("/create", response_model=User)
async def create_users(user: UserCreate):
    return create_user(user)

@router.put("/update",response_model=User)
async def update_users(user: User):
    return update_user(user)

@router.delete("/delete",response_model=dict)
async def delete_users(user: User):
    return delete_user(user)

@router.get("/", response_model=list[User])
async def read_users():
    return get_all_users()