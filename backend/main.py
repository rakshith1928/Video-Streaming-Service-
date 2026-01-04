from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.mount("/media", StaticFiles(directory="../hls"),name="media")
@app.get("/")
def home():
    return {"message": "Streaming Service API is running"}
  