import os
import uuid
from datetime import datetime
from pathlib import Path
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from core.dependencies import get_current_user

# Definir el directorio base para los archivos
BASE_UPLOAD_DIR = Path("uploads")

router = APIRouter()

@router.post("/upload")
async def upload_image(
    file: UploadFile = File(...),
    current_user=Depends(get_current_user)  # Validar autenticación
):
    try:
        # Validar que el archivo sea una imagen
        if not file.content_type.startswith("image/"):
            raise HTTPException(status_code=400, detail="Only image files are allowed")

        # Obtener la fecha actual
        now = datetime.utcnow()
        year = now.strftime("%Y")
        month = now.strftime("%m")
        day = now.strftime("%d")

        # Crear la estructura de carpetas según la fecha
        upload_path = BASE_UPLOAD_DIR / year / month / day
        upload_path.mkdir(parents=True, exist_ok=True)  # Crear directorios si no existen

        # Generar un nombre único para la imagen
        file_extension = file.filename.split(".")[-1]  # Obtener extensión
        unique_filename = f"{uuid.uuid4()}.{file_extension}"  # Nombre con UUID

        # Ruta completa del archivo
        file_path = upload_path / unique_filename

        # Guardar el archivo en la estructura definida
        with file_path.open("wb") as buffer:
            buffer.write(await file.read())

        return {
            "message": "File uploaded successfully",
            "filename": unique_filename,
            "path": str(file_path),
            "user": current_user["username"]  # Muestra el usuario autenticado
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving file: {str(e)}")

