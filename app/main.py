import os
import shutil

import requests
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image

app = FastAPI()

ORIGINS = ["http://localhost:3000", "http://localhost"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# upload dir
UPLOAD_DIR = "atencion_al_usuario_insumos"
os.makedirs(UPLOAD_DIR, exist_ok=True)

NGINX_DIR = "https://static-zapopan-api.appsuzu.fun"


@app.get("/api/insumos/get-file")
def getFile():
    compress = requests.get(NGINX_DIR + "/compress/")
    return {"images": compress.json()}


@app.post("/api/insumos/upload-file")
def read_root(
    file: UploadFile = File(...),
):

    filename_not_extension = file.filename.split(".")
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
        file_location = f"{UPLOAD_DIR}/original/original_{file.filename}"
        save_image(file_location, file, filename_not_extension[0])
        return {
            "message": "File uploaded successfully!",
            "filename": file.filename,
            "content_type": file.content_type,
        }
    else:
        raise HTTPException(status_code=400, detail="Archivo no soportado")


def save_image(file_location: str, file: UploadFile, filename_not_extension: str):
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    with Image.open(file_location) as img:
        compressed_location = os.path.join(
            UPLOAD_DIR + "/compress/", f"compress_{filename_not_extension}.webp"
        )
        img.thumbnail((300, 300))
        img.convert("RGB").save(
            compressed_location, optimize=True, quality=70, format="WEBP"
        )


def save_pdf(file_location, file: UploadFile, zoom_x=0.75, zoom_y=0.75):
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
