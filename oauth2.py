from jose import JWTError, jwt
from datetime import datetime,timedelta,timezone
import schemas
from fastapi import Depends,status, HTTPException
from fastapi.security import OAuth2PasswordBearer
import models
from sqlalchemy.orm import Session
import models, schemas
from database import get_db


SECRET_KEY="hello"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTE = 10 

oauth2_scheme = OAuth2PasswordBearer(tokenUrl= 'login')

def create_access_token(data:dict):
    to_encode=data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTE)
    print(expire)
    to_encode.update({"exp":expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token:str, credentials_exception):
    try:
        payload = jwt.decode(token,SECRET_KEY,ALGORITHM)

        id:int = payload.get("user_id")

        if id is None:
            raise credentials_exception
        token_data = schemas.token_data(id = id)
    except JWTError:
        raise credentials_exception
    
    return token_data
    

def get_current_user(token: str = Depends(oauth2_scheme),db: Session = Depends(get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED ,detail=f"Could not available credentails",
                                          headers={"WW-Authenticate":"Bearer"})

    token = verify_access_token(token,credentials_exception)
    user = db.query(models.user).filter(models.user.id == token.id).first()
    return user





