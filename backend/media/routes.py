from fastapi import APIRouter, HTTPException, Header
from fastapi.responses import FileResponse
import os
from auth.utils import decode_token # import decoder token function from client token 
router = APIRouter()
BASE_HLS_PATH = os.path.abspath("../hls")

@router.get("/master.m3u8")
def get_master_playlist(authorization: str = Header(None)):
    
    if authorization is None:
        raise HTTPException(status_code=401, detail="Authorization header missing")
    
    #Extarcting token from Bearer token
    _,token=authorization.split()
    decode_token(token)
    
    # then u  can give master playlist to user player
    path = os.path.join(BASE_HLS_PATH,"master.m3u8")
    if not os.path.exists(path):
        raise HTTPException(status_code=404,detail="Master playlist not found")
    return FileResponse(path,media_type="application/vnd/apple.mpegurl")

@router.get("/{quality}/{filename}")
def get_hls_file(quality : str,filename: str, authorization: str = Header(None)):
    if authorization is None:
        raise HTTPException(status_code=401, detail="Authorization header missing")
    
    #Extarcting token from Bearer token(client)
    _,token=authorization.split()
    payload = decode_token(token)
    
    user_max_quality = payload.get("max_quality")
    # to check if user max allowed quality is req quality
    if int(quality[:-1]) > int(user_max_quality[:-1]):
        raise HTTPException(status_code=403,detail="Requested quality exceeds user's maximum alowwed quyality")    
    
    path = os.path.join(BASE_HLS_PATH,quality,filename)
    if not os.path.exists(path):
        raise HTTPException(status_code=404,detail="Requested file not found")
    if filename.endswith(".m3u8"):
        media_type = "application/vnd.apple.mpegurl"
    else:
        media_type="video/MP2T"
        
    return FileResponse(path,media_type = media_type)