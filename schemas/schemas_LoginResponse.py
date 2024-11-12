import uuid
from pydantic import BaseModel
from typing import Optional
from datetime import date
from fastapi import APIRouter, UploadFile, File
class LoginResponse(BaseModel):
    message: str
    user_id: Optional[str] = None 