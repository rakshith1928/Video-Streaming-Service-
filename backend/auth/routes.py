from fastapi import APIRouter , HTTPException
from jose import JWTError, jwt
from pydantic import BaseModel 
from config import SECRET_KEY , ALGORITHM , ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_DAYS
from database import SessionLocal
from models import User, RefreshToken
from datetime import datetime, timedelta
router = APIRouter()

users = {
  "lazy":{"password":"1234","max_quality":"1080p"},
  "guest":{"password":"guest","max_quality":"720p"}
}
#Simulated DB for refresh tokens
refresh_token_store = {}
# Load environment variables from .env file
#load_dotenv()

class LoginRequest(BaseModel):
    username : str
    password : str
    
    
@router.post("/login")
def login(req : LoginRequest):
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.username == req.username).first()
        if user is None or user.password != req.password:
            raise HTTPException(status_code=401, detail="Invalid username or password")
    finally:
        db.close()
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
    db.query(RefreshToken).filter(RefreshToken.username == req.username).delete()
    new_token = RefreshToken(username=req.username, token=refresh_token)
    db.add(new_token)
    db.commit()
    
    
    return {"access token": access_token, "refresh token": refresh_token}
  
#create reqmodel

class RefreshRequest(BaseModel):
    refresh_token: str
    

  
@router.post("/refresh")
def refresh_token(request: RefreshRequest):
    db = SessionLocal()
    try:
        payload = jwt.decode(request.refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("type")!="refresh":
            raise HTTPException(status_code=401, detail="Invalid token type")
        
        username = payload["username"]
        #Check if token is in store
        stored = db.query(RefreshToken).filter(RefreshToken.username == username).first()
        if not stored or stored.token != request.refresh_token:
            raise HTTPException(status_code=401, detail="Invalid refresh token")

        
        access_expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        new_access_playload = {
            "username" : payload["username"],
            "max_quality": users[payload["username"]]["max_quality"],
            "type": "accesss",
            "exp": access_expire
            
        }
        new_access_token = jwt.encode(new_access_playload, SECRET_KEY, algorithm=ALGORITHM)
        #Refresh Token Roatation
        refresh_expire = datetime.utcnow()+timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
        new_refresh_payload = {
            "username": username,
            "type": "refresh",
            "exp": refresh_expire
        }
        new_refresh_token = jwt.encode(new_refresh_payload,SECRET_KEY, algorithm=ALGORITHM)
        # replace old one
        refresh_token_store[username] = new_refresh_token
        
        return {"access_token": new_access_token, "refresh_token": new_refresh_token}
    
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired refresh token")
    
@router.post("/logout")
def logout(request : RefreshRequest):
    try:
        payload = jwt.encode(request.refresh_token,SECRET_KEY , algorithms=[ALGORITHM])
        username = payload["username"]
        refresh_token_store.pop(username,None)
        return {"message": "Logged out successfully"}
    except JWTError:
        raise HTTPException(status_code=401,detail="Invalid Token")
        
          
    
          
  
    