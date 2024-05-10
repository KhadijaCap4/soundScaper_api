from pydantic import BaseModel
import uuid

class Todo(BaseModel):
    id: uuid.UUID
    Title: str
    Description: str
    Completed: bool

class TodoCreate(BaseModel):
    Title: str
    Description: str
    
class TodoUpdate(BaseModel):
    Title: str
    Description: str
    Completed: bool
