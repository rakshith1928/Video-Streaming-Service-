from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from auth.routes import router as auth_router
import os 


app = FastAPI()
BASE_HLS_PATH = os.path.abspath("../hls")

#Auth Routes
app.include_router(auth_router , prefix="/auth")

@app.get("/")
def home():
    return {"message": "Streaming Service API is running"}

@app.get("/media/master.m3u8")
def get_master_playlist():
    path = os.path.join(BASE_HLS_PATH,"master.m3u8")
    if not os.path.exists(path):
        raise HTTPException(status_code=404)
    return FileResponse(path,media_type="application/vnd/apple.mpegurl")

@app.get("/media/{quality}/{filename}")
def get_hls_file(quality : str,filename: str):
    path = os.path.join(BASE_HLS_PATH,quality,filename)
    if not os.path.exists(path):
        raise HTTPException(status_code=404)
    if filename.endswith(".m3u8"):
        media_type = "application/vnd.apple.mpegurl"
    else:
        media_type="video/MP2T"
        
    return FileResponse(path,media_type = media_type)




  