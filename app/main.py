import os
import shutil

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image

app = FastAPI()

ORIGINS = [
    "http://localhost:3000",
    "http://localhost"
]

app.add_middleware(CORSMiddleware, allow_origins=ORIGINS, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

UPLOAD_DIR = "atencion_al_usuario_insumos"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.post("/api/insumos/upload-file")
def read_root(
    file: UploadFile = File(...),
):
    if file.content_type == "application/pdf":
        file_location = f"{UPLOAD_DIR}/original_{file.filename}"
        save_pdf(file_location, file)
        return {
            "message": "PDF uploaded successfully!",
        }
    elif (
        file.content_type == "image/jpeg"
        or file.content_type == "image/wepb"
        or file.content_type == "image/png"
        or file.content_type == "image/jpg"
    ):
        file_location = f"{UPLOAD_DIR}/original_{file.filename}"
        save_image(file_location, file)
        return {
            "message": "File uploaded successfully!",
            "filename": file.filename,
            "content_type": file.content_type,
        }
    else:
        raise HTTPException(status_code=400, detail="Archivo no soportado")


def save_image(file_location: str, file: UploadFile):
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    with Image.open(file_location) as img:
        compressed_location = os.path.join(UPLOAD_DIR, f"compress_{file.filename}.webp")
        img.convert("RGB").save(
            compressed_location, optimize=True, quality=10, format="WEBP"
        )


def save_pdf(file_location, file: UploadFile, zoom_x=0.75, zoom_y=0.75):
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
