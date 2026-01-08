from fastapi import FastAPI
from auth.routes import router as auth_router
from media.routes import router as media_router

app = FastAPI()

#Auth Routes ending with auth/
app.include_router(auth_router , prefix="/auth")

#Media routes from media/routes.py ending with media/
app.include_router(media_router , prefix="/media")

@app.get("/")
def home():
    return {"message": "Streaming Service API is running"}





  