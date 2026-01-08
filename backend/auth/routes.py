from fastapi import APIRouter , HTTPException
from jose import JWTError, jwt
from pydantic import BaseModel 
from dotenv import load_dotenv
import os

router = APIRouter()

users = {
  "lazy":{"password":"1234","max_quality":"1080p"},
  "guest":{"password":"guest","max_quality":"720p"}
}
# Load environment variables from .env file
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")

class LoginRequest(BaseModel):
    username : str
    password : str
    
@router.post("/login")
def login(req : LoginRequest):
    user = users.get(req.username)
    if not user or user["password"] != req.password:
      raise HTTPException(status_code= 401, detail="Invalid username or password")
    
    token_data = {
      "username": req.username,
      "max_quality": user["max_quality"]
    }
    token = jwt.encode(token_data, SECRET_KEY , algorithm=ALGORITHM)
    return {"access token": token}
