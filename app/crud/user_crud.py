from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user_schema import UserCreate
from app.utils.hashing import hash_password, verify_password

def create_user(db: Session, user: UserCreate):
    hash_pwd = hash_password(user.password)

    db_user = User(
        name=user.name,
        email=user.email,
        password=hash_pwd,
        role=user.role
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user

def authenticate_user(db:Session, email:str, password: str):
    user = db.query(User).filter(User.email == email).first()

    if not user:
        return None
    
    if not verify_password(password, user.password):
        return None
    
    return user