from jose import jwt,JWTError
from datetime import datetime,timedelta,timezone
from fastapi import FastAPI,HTTPException,Depends
from fastapi.security import OAuth2PasswordBearer

SECREAT_KEY  = "mysecreat"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MMINUTE = 30

oauth2_schema = OAuth2PasswordBearer(tokenUrl="login")

#token create
def create_token(data:dict):
    to_encode = data.copy()
    
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MMINUTE)
    to_encode.update({"exp":expire})
    
    return jwt.encode(to_encode,SECREAT_KEY,algorithm=ALGORITHM)

def verify_token(token:str=Depends(oauth2_schema)):
    try:
        payload = jwt.decodes(token,SECREAT_KEY,algorithm = ALGORITHM)
        return payload
    except JWTError:
        raise HTTPException(status_code=401,detail="invalid token")

        
     