
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
import os
from app.core.config import Config

router = APIRouter()

OUTPUT_DIR =  Config.UPLOAD_DIR

@router.get("/{file_name}")
async def download_file(file_name: str):
    file_path = os.path.join(OUTPUT_DIR, file_name)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(file_path, media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', filename=file_name)

