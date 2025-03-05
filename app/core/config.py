import os

class Config:
    UPLOAD_DIR = os.getenv("UPLOAD_DIR", "./data/uploads/")
    OUTPUT_DIR = os.getenv("OUTPUT_DIR", "./output/processed/")
    