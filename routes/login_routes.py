from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from services.login_service import authenticate_user
from schemas.schemas_login import LoginRequest, LoginResponse
from db.database import get_db

router = APIRouter()

@router.post("/login", response_model=LoginResponse, tags=["Authentication"])
def login_endpoint(login_data: LoginRequest, db: Session = Depends(get_db)):
    auth_response = authenticate_user(login_data.email, login_data.password, db)
    return LoginResponse(access_token=auth_response["access_token"], token_type=auth_response["token_type"])
