from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from sqlalchemy.orm import Session
from typing import List
import json

from .database import get_db
from .crud import post_composition, upload_to_cloudinary
from .Models.models import CompositionOut

router = APIRouter(tags=["Composition"])




# --- POST-эндпоинт ---
@router.post("/composition-with-images/", response_model=CompositionOut)
async def create_composition_with_images(
    title: str = Form(...),
    author: str = Form(...),
    description: str = Form(None),
    type: str = Form(None),
    cover: UploadFile = File(...),            # Обложка
    chapters_data: str = Form(...),           # JSON с главами (без картинок)
    files: List[UploadFile] = File(...),      # Все картинки всех глав в порядке
    db: Session = Depends(get_db)
):
    # Загружаем обложку
    cover_url = await upload_to_cloudinary(cover, folder=title)

    # Парсим главы
    chapters_json = json.loads(chapters_data)

    # Загружаем все картинки глав
    file_index = 0
    for chapter in chapters_json:
        images = []
        for _ in chapter.get("images", []):  # по количеству картинок в главе
            file = files[file_index]
            file_index += 1
            image_url = await upload_to_cloudinary(file, folder=f"{title}/chapter{chapter['chapter_number']}")
            images.append({"url": image_url})
        chapter["images"] = images

    # Сохраняем композицию в БД
    composition = post_composition(
        db=db,
        title=title,
        author=author,
        description=description,
        type=type,
        cover_url=cover_url,
        chapters=chapters_json
    )

    if composition is None:
        raise HTTPException(status_code=400, detail="Composition with this title already exists")

    return composition
