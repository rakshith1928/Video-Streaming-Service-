from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
import os

router = APIRouter()
BASE_HLS_PATH = os.path.abspath("../hls")

@router.get("/master.m3u8")
def get_master_playlist():
    path = os.path.join(BASE_HLS_PATH,"master.m3u8")
    if not os.path.exists(path):
        raise HTTPException(status_code=404,detail="Master playlist not found")
    return FileResponse(path,media_type="application/vnd/apple.mpegurl")

@router.get("/{quality}/{filename}")
def get_hls_file(quality : str,filename: str):
    path = os.path.join(BASE_HLS_PATH,quality,filename)
    if not os.path.exists(path):
        raise HTTPException(status_code=404,detail="Requested file not found")
    if filename.endswith(".m3u8"):
        media_type = "application/vnd.apple.mpegurl"
    else:
        media_type="video/MP2T"
        
    return FileResponse(path,media_type = media_type)