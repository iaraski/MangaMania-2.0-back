import cloudinary
from sqlalchemy.orm import Session
from .Models.models import User, Composition, CompositionChapter, ChapterImage
from passlib.context import CryptContext
from typing import Optional, List
from fastapi import HTTPException, UploadFile
from cloudinary.uploader import upload as cloudinary_upload

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ---------- User ----------
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

def get_user(db: Session, user_id: int) -> Optional[User]:
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_username(db: Session, username: str) -> Optional[User]:
    return db.query(User).filter(User.username == username).first()

def get_user_by_email(db: Session, email: str) -> Optional[User]:
    return db.query(User).filter(User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 200) -> List[User]:
    return db.query(User).offset(skip).limit(limit).all()

def create_user(db: Session, username: str, email: str, hashed_password: str) -> User:
    db_user = User(username=username, email=email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()

# ---------- Composition ----------
def get_composition(db: Session, id: int) -> Optional[Composition]:
    return db.query(Composition).filter(Composition.id == id).first()

def get_compositions(db: Session, skip: int = 0, limit: int = 10) -> List[Composition]:
    return db.query(Composition).offset(skip).limit(limit).all()

def post_composition(
    db: Session,
    title: str,
    author: str,
    description: Optional[str] = None,
    type: Optional[str] = None,
    cover_url: Optional[str] = None,
    chapters: Optional[List[dict]] = None
) -> Optional[Composition]:
    if db.query(Composition).filter(Composition.title == title).first():
        return None

    new_composition = Composition(
        title=title,
        author=author,
        description=description,
        type=type,
        cover_url=cover_url
    )
    db.add(new_composition)

    for chapter_data in (chapters or []):
        chapter = CompositionChapter(
            chapter_number=chapter_data["chapter_number"],
            title=chapter_data["title"],
            content=chapter_data["content"],
            composition=new_composition
        )
        db.add(chapter)
        for image_data in chapter_data.get("images", []):
            image = ChapterImage(url=image_data["url"], chapter=chapter)
            db.add(image)

    db.commit()
    db.refresh(new_composition)
    return new_composition

def delete_composition(db: Session, id: int) -> bool:
    composition = db.query(Composition).filter(Composition.id == id).first()
    if not composition:
        return False
    db.delete(composition)
    db.commit()
    return True

# --- Вспомогательная функция загрузки в Cloudinary ---


async def upload_to_cloudinary(file: UploadFile, folder: str):
    result = cloudinary.uploader.upload(file.file, folder=folder)
    return result  # вернёт dict с 'secure_url' и 'public_id'