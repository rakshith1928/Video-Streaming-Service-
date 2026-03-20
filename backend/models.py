from sqlalchemy import Column, Integer, String
from database import Base
 
class User(Base):
  __tablename__ = "users"
 
  id = Column(Integer, primary_key=True, index=True)
  username = Column(String, index=True)
  password = Column(String)
  hashed_password = Column(String)
    
class RefreshToken(Base):
  __tablename__ = "refresh_tokens"
  
  id = Column(Integer, primary_key=True, index=True)
  username = Column(String, index=True)
  token = Column(String, unique=True)