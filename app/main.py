from fastapi import FastAPI, File, UploadFile, Form
import shutil
import os
from typing import Any

app = FastAPI()

UPLOAD_DIR = "atencion_al_usuario_insumos"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.post("/api/insumos/upload-file")
def read_root(
    file: UploadFile = File(...),
    username: str = Form(...),
    description: str = Form(None),
):
    file_location = f"{UPLOAD_DIR}/{file.filename}"
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {
        "message": "File uploaded successfully!",
        "filename": file.filename,
        "content_type": file.content_type,
        "uploaded_by": username,
        "description": description,
    }
