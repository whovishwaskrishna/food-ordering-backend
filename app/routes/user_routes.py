from fastapi import APIRouter,Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.user_schema import UserCreate, UserResponse, UserLogin, TokenResponse
from app.core.security import create_access_token, get_current_user
from app.crud.user_crud import create_user,authenticate_user
from app.models.user import User

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/register", response_model=UserResponse)
def register(user: UserCreate, db:Session = Depends(get_db)):
    return create_user(db,user)


@router.post("/login", response_model=TokenResponse)
def login(user:UserLogin, db: Session=Depends(get_db)):
    db_user = authenticate_user(db, user.email, user.password)

    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid Credential")
    
    token = create_access_token({"sub":db_user.email})

    return {"access_token":token}

@router.get("/me", response_model=UserResponse)
def get_me(current_user:User=Depends(get_current_user)):
    return current_user