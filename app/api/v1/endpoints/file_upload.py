from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from app.services.processing import process_excel_file
from app.utils.file_handler import save_upload_file
from app.core.config import Config

router = APIRouter()

UPLOAD_DIR = Config.UPLOAD_DIR

@router.post("/file")
def upload_file(file: UploadFile = File(...)):
    file_path = save_upload_file(file, UPLOAD_DIR)
    if not file_path:
        raise HTTPException(status_code=500, detail="File upload failed")
    output_file, plots = process_excel_file(file_path)
    return JSONResponse(content={
        "processed_file": output_file,
        "plots": plots
    })
