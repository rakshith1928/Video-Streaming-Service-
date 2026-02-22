from fastapi import APIRouter , HTTPException
from jose import JWTError, jwt
from pydantic import BaseModel 
from config import SECRET_KEY , ALGORITHM , ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_DAYS
from datetime import datetime, timedelta
router = APIRouter()

users = {
  "lazy":{"password":"1234","max_quality":"1080p"},
  "guest":{"password":"guest","max_quality":"720p"}
}
# Load environment variables from .env file
#load_dotenv()

class LoginRequest(BaseModel):
    username : str
    password : str
    
    
@router.post("/login")
def login(req : LoginRequest):
    user = users.get(req.username)
    if not user or user["password"] != req.password:
      raise HTTPException(status_code= 401, detail="Invalid username or password")
    #expire token after 30 minutes
    access_expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    access_payload = {
      "username": req.username,
      "max_quality": user["max_quality"],
      "type": "access",
      "exp": access_expire
    }
    access_token = jwt.encode(access_payload, SECRET_KEY , algorithm=ALGORITHM)
    
    #refresh token
    refresh_expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    refresh_payload = {
      "username": req.username,
      "type": "refresh",
      "exp": refresh_expire
    } 
    refresh_token = jwt.encode(refresh_payload, SECRET_KEY , algorithm=ALGORITHM)
    
    return {"access token": access_token, "refresh token": refresh_token}
  
#create reqmodel

class RefreshRequest(BaseModel):
    refresh_token: str

  
@router.post("/refresh")
def refresh_token(request: RefreshRequest):
    try:
        payload = jwt.decode(request.refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("type")!="refresh":
            raise HTTPException(status_code=401, detail="Invalid token type")
        
        access_expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        new_access_playload = {
            "username" : payload["username"],
            "max_quality": users[payload["username"]]["max_quality"],
            "type": "accesss",
            "exp": access_expire
            
        }
        new_access_token = jwt.encode(new_access_playload, SECRET_KEY, algorithm=ALGORITHM)
        return {"access_token": new_access_token}
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired refresh token")
        
          
    
          
  
    