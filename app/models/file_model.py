from pydantic import BaseModel

class FileResponseModel(BaseModel):
    processed_file: str
    plots: list[str]
    