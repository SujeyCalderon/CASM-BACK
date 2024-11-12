import uuid
from pydantic import BaseModel
from typing import Optional
from datetime import date
from fastapi import APIRouter, UploadFile, File
class LoginRequest(BaseModel):
    email: str
    password: str