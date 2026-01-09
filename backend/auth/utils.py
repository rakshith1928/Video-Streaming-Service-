from jose import JWTError,jwt
from fastapi import HTTPException, status
from config import SECRET_KEY, ALGORITHM

def decode_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or Expired token"
        )