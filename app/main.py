from fastapi import FastAPI
from app.api.v1.endpoints import file_upload, download
from app.core.config import Config 
import os

app = FastAPI(title="Excel File Processor API", version="1.0.0")

os.makedirs(Config.OUTPUT_DIR, exist_ok=True)
os.makedirs(Config.UPLOAD_DIR, exist_ok=True)

app.include_router(file_upload.router, prefix="/upload", tags=["File Upload"])
app.include_router(download.router, prefix="/download", tags=["File Download"])

@app.get("/")
async def root():
    return {"message": "Welcome to the Excel File Processor API!"}