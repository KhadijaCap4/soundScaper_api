from fastapi import APIRouter, HTTPException
from typing import List
from classes.schemas_dto import User, UserNoID
import uuid

router= APIRouter(
    prefix='/users',
    tags=["Users"]
)

users = [
    User(id=uuid.uuid4(), username="Dija", email="dija@gmail.com", password="Dija"),
    User(id=uuid.uuid4(), username="Oumar", email="oumar@gmail.com", password="Oumar"),
    User(id=uuid.uuid4(), username="Daouda", email="daouda@gmail.com", password="Oumar")
]

@router.get('/users', response_model=List[User])
async def get_user():
    return users

@router.post('/users', response_model=User, status_code=201)
async def create_user(givenUsername: UserNoID, givenEmail: UserNoID, givenPassword: UserNoID):
    generatedId = uuid.uuid4()
    newUser = User(id=generatedId, username=givenUsername.username)  
    users.append(newUser)
    return newUser

@router.get('/users/{user_id}', response_model=User)
async def get_user_by_ID(user_id: uuid.UUID):  # Change data type to uuid.UUID
    for user in users:
        if user.id == user_id:
            return user
    raise HTTPException(status_code=404, detail="User not found")

@router.patch('/users/{user_id}', status_code=204)
async def modify_user_title(user_id: uuid.UUID, modifiedUser: UserNoID):
    for user in users:
        if user.id == user_id:
            user.username = modifiedUser.username,
            user.email = modifiedUser.email,
            user.password = modifiedUser.password
            return
    raise HTTPException(status_code=404, detail="User not found")

@router.delete('/users/{user_id}', status_code=204)
async def delete_user(user_id: uuid.UUID):  # Change data type to uuid.UUID
    for user in users:
        if user.id == user_id:
            users.remove(user)
            return
    raise HTTPException(status_code=404, detail="User not found")
