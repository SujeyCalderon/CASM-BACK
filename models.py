import uuid
from pydantic import BaseModel
from typing import Optional
from datetime import date
from fastapi import APIRouter, UploadFile, File

class User(BaseModel):
    id: str = None  
    name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    specialty: Optional[str] = None
    phone: Optional[str] = None
    role: Optional[str] = None
    document: Optional[str] = None
    address: Optional[str] = None
    is_premium: Optional[bool] = False 

    def __init__(self, **data):
        super().__init__(**data)
        if not self.id:
            self.id = str(uuid.uuid4())

class Publication(BaseModel):
    id: str = None  
    user_id: Optional[str] = None  
    description: Optional[str] = None
    image: Optional[str] = None  

    def __init__(self, **data):
        super().__init__(**data)
        if not self.id:
            self.id = str(uuid.uuid4())
class LoginRequest(BaseModel):
    email: str
    password: str

class LoginResponse(BaseModel):
    message: str
    user_id: Optional[str] = None 

class Notes(BaseModel):
    id: Optional[str] = None
    user_id: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    creation_date: Optional[date] = None
    modification_date: Optional[date] = None
    def __init__(self, **data):
        super().__init__(**data)
        if not self.id:
            self.id = str(uuid.uuid4()) 

class Directory(BaseModel):
    id: str = None  
    user_id: Optional[str] = None  
    name: Optional[str] = None
    description: Optional[str] = None
    phone: Optional[str] = None
    direction: Optional[str] = None
    image: Optional[str] = None  
    email: Optional[str] = None

    def __init__(self, **data):
        super().__init__(**data)
        if not self.id:
            self.id = str(uuid.uuid4())
class Favorites(BaseModel):
    id: str = None 
    user_id: Optional[str] = None  
    favorite_user_id: Optional[str] = None 
    publication_id : Optional[str] = None 

    def __init__(self, **data):
        super().__init__(**data)
        if not self.id:
            self.id = str(uuid.uuid4()) 

class Role(BaseModel):
    id: str = None  
    name: Optional[str] = None  

    def __init__(self, **data):
        super().__init__(**data)
        if not self.id:
            self.id = str(uuid.uuid4())