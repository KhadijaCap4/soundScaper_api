from fastapi import APIRouter, HTTPException, status
from typing import List, Optional
from pydantic import BaseModel
import uuid
from database.firebase import db

router = APIRouter(
    prefix='/todos',
    tags=["Todos"]
)

class TodoCreate(BaseModel):
    Title: str
    Description: str

class TodoUpdate(BaseModel):
    Title: str
    Description: str
    Completed: bool
    
class Todo(BaseModel):
    id: Optional[str]
    Title: str
    Description: str
    Completed: Optional[bool]

@router.get('', response_model=List[Todo])
async def get_todos():
    todos = db.child("Task").get().val()
    if todos is None:
        return []  
    todo_list = []
    for key, value in todos.items():
        todo = Todo(id=key, **value)
        todo_list.append(todo)
    return todo_list

@router.get('/{todo_id}', response_model=Todo)
async def get_todo_by_id(todo_id: str):
    todo = db.child("Task").child(todo_id).get().val()
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return Todo(id=todo_id, **todo)

@router.post('', response_model=TodoCreate, status_code=status.HTTP_201_CREATED)
async def create_todo(todo_data: TodoCreate):
    new_id = str(uuid.uuid4())
    todo_dict = {
        "Title": todo_data.Title,
        "Description": todo_data.Description,
        "Completed": False
    }
    db.child("Task").child(new_id).set(todo_dict)
    return TodoCreate(**todo_dict)

@router.patch('/{todo_id}', response_model=TodoUpdate)
async def update_todo(todo_id: str, todo_data: TodoUpdate):
    todo = db.child("Task").child(todo_id).get().val()
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    updated_todo = todo.copy()
    updated_todo.update(todo_data.dict())
    db.child("Task").child(todo_id).update(updated_todo)
    return TodoUpdate(**updated_todo)

@router.delete('/{todo_id}', status_code=204)
async def delete_todo(todo_id: str):
    todo = db.child("Task").child(todo_id).get().val()
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    db.child("Task").child(todo_id).remove()
