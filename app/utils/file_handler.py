import os
from fastapi import UploadFile

def save_upload_file(upload_file: UploadFile, destination_folder: str) -> str:
    file_path = os.path.join(destination_folder, upload_file.filename)
    with open(file_path, "wb") as buffer:
        buffer.write(upload_file.file.read())
    return file_path
