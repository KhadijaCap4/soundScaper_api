from pydantic import BaseModel
import uuid

class Music(BaseModel):
    id: uuid.UUID  # Change data type to uuid.UUID
    title: str

class MusicNoID(BaseModel):
    title: str

class User(BaseModel):
    id: uuid.UUID
    username: str
    email: str
    password: str

class UserNoID(BaseModel):
    username: str
    email: str
    password: str

class UserAuth(BaseModel):
    email: str
    password: str