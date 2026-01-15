from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import yt_dlp
import os
import uuid

app = FastAPI()

# Allow your Blogger site to connect to this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"status": "VPS Online", "message": "GitHub Codespace API is running"}

@app.get("/download")
async def download_shorts(url: str = Query(..., description="YouTube Shorts URL")):
    # Create a unique filename for the session
    file_id = str(uuid.uuid4())[:8]
    output_path = f"video_{file_id}.mp4"

    # Professional yt-dlp configuration to bypass blocks
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'outtmpl': output_path,
        'quiet': True,
        'no_warnings': True,
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'referer': 'https://www.google.com/',
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
        # Check if file was successfully created
        if os.path.exists(output_path):
            return FileResponse(
                path=output_path, 
                media_type='video/mp4', 
                filename="youtube_shorts.mp4"
            )
        else:
            raise HTTPException(status_code=404, detail="VPS failed to generate file")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))