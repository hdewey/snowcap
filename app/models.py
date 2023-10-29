from fastapi import File, UploadFile, Form

from pydantic import BaseModel

class QuickGenRequest(BaseModel):
    property_id: str
    description: str

class Recording(BaseModel):
    file: UploadFile
    property_id: str

def get_recording(
    file: UploadFile = Form(...),
    property_id: str = Form(...)
) -> Recording:
    return Recording(file=file, property_id=property_id)