from fastapi import FastAPI
from app.api.v1.endpoints import file_upload, download
from app.core.config import Config 
import os
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import FastAPI, Request, Form, File, UploadFile, HTTPException
import shutil
from app.utils.file_handler import save_upload_file
from app.core.config import Config
from app.services.processing import process_excel_file
from fastapi.responses import FileResponse


UPLOAD_DIR = Config.UPLOAD_DIR

app = FastAPI(title="Excel File Processor API", version="1.0.0")

os.makedirs(Config.OUTPUT_DIR, exist_ok=True)
os.makedirs(Config.UPLOAD_DIR, exist_ok=True)

# app.include_router(file_upload.router, prefix="/upload", tags=["File Upload"])
# app.include_router(download.router, prefix="/download", tags=["File Download"])

# Make sure this matches the folder where you placed index.html
templates = Jinja2Templates(directory="app/templates")

# Route for showing the HTML form
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):  # <-- make sure 'request' is included here
    return templates.TemplateResponse("index.html", {"request": request})


# Route for handling the form submission
@app.post("/submit")
async def submit_form(
    experiment_name: str = Form(...),
    has_control: bool = Form(False),
    control_name: str = Form(None),
    has_normalization: bool = Form(False),
    normalization_name: str = Form(None),
    file: UploadFile = File(...)
):
    
    file_path = save_upload_file(file, UPLOAD_DIR)
    if not file_path:
        raise HTTPException(status_code=500, detail="File upload failed")
    output_file = process_excel_file(file_path, control_name, normalization_name,  experiment_name, has_control, has_normalization)


    return FileResponse(output_file, media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', filename=f'{experiment_name}.xlsx')
