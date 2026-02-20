from datetime import datetime,timedelta
from jose import JWTError, jwt
from fastapi import Depends,HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User

SECRET_KEY = "mySecretKey123"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_TIME = 60 # 1 hours

security = HTTPBearer()

def create_access_token(data:dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_TIME)
    to_encode.update({"exp": expire})
    token = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return token

def decode_access_token(token:str):
    try:
        payload = jwt.decode(token,SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None
    

def get_current_user(credentials: HTTPAuthorizationCredentials= Depends(security), db: Session = Depends(get_db)):
    token = credentials.credentials
    payload = decode_access_token(token)

    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or Expired token")
    
    email = payload.get("sub")

    user = db.query(User).filter(User.email == email).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user