from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    avatar_url = Column(String, nullable=True)
    avatar_public_id = Column(String, nullable=True)

class Composition(Base):
    __tablename__ = "compositions"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False, unique=True)
    author = Column(String, nullable=False)
    description = Column(String, nullable=True)
    type = Column(String, nullable=True)
    cover_url = Column(String, nullable=True)
    likes = Column(Integer, default=0)
    genre = Column(String, nullable=False)
    year = Column(Integer, nullable=False)

    chapters = relationship(
        "CompositionChapter",
        back_populates="composition",
        cascade="all, delete-orphan"
    )

class CompositionChapter(Base):
    __tablename__ = "composition_chapters"
    id = Column(Integer, primary_key=True, index=True)
    composition_id = Column(Integer, ForeignKey("compositions.id"), nullable=False)
    chapter_number = Column(Integer, nullable=False)

    composition = relationship("Composition", back_populates="chapters")
    images = relationship(
        "ChapterImage",
        back_populates="chapter",
        cascade="all, delete-orphan"
    )

class ChapterImage(Base):
    __tablename__ = "chapter_images"
    id = Column(Integer, primary_key=True, index=True)
    chapter_id = Column(Integer, ForeignKey("composition_chapters.id"), nullable=False)
    url = Column(String, nullable=False)

    chapter = relationship("CompositionChapter", back_populates="images")


