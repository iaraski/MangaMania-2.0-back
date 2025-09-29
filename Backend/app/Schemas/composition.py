from ast import List
from typing import Optional
from pydantic import BaseModel


class ChapterImageOut(BaseModel):
    id: int
    url: str
    class Config:
        from_attributes = True

class CompositionChapterOut(BaseModel):
    id: int
    chapter_number: int
    images: List[ChapterImageOut] = []
    class Config:
        from_attributes = True

class CompositionOut(BaseModel):
    id: int
    title: str
    author: str
    description: Optional[str]
    type: Optional[str]
    cover_url: Optional[str]
    chapters: List[CompositionChapterOut] = []
    genre :str
    year : int
    likes : int
    class Config:
        from_attributes = True

class ChapterImageCreate(BaseModel):
    url: str  # Сюда будет записываться ссылка после загрузки в облако

class CompositionChapterCreate(BaseModel):
    chapter_number: int
    content: str
    images: List[ChapterImageCreate] = []

class CompositionCreate(BaseModel):
    title: str
    author: str
    description: Optional[str] = None
    type: Optional[str] = None
    cover_url: Optional[str] = None
    genre: str
    year: int
    chapters: List[CompositionChapterCreate] = []


