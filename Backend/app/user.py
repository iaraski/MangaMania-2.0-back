# app/user.py
import cloudinary
from fastapi import APIRouter, Depends, HTTPException, UploadFile, status
from sqlalchemy.orm import Session


from .database import SessionLocal, get_db
from .Models.models import UserCreate, UserLogin, UserOut, Token, User, AuthResponse
from .crud import get_user_by_username, get_user_by_email, create_user, hash_password, upload_to_cloudinary, verify_password,delete_user
from .auth import create_access_token, get_current_user

router = APIRouter(prefix="/auth", tags=["auth"])



@router.post("/register", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
def register(payload: UserCreate, db: Session = Depends(get_db)):
    if get_user_by_username(db, payload.username):
        raise HTTPException(status_code=400, detail="Username already taken")
    if get_user_by_email(db, payload.email):
        raise HTTPException(status_code=400, detail="Email already registered")

    user = create_user(
        db,
        username=payload.username,
        email=payload.email,
        hashed_password=hash_password(payload.password),
    )

    token = create_access_token({"sub": user.username})

    return {
        "token": token,
        "user": user,  
    }

@router.post("/login", response_model=Token)
def login(payload: UserLogin, db: Session = Depends(get_db)):
    user = get_user_by_username(db, payload.username)
    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    token = create_access_token({"sub": user.username, "uid": user.id})
    return {
        "token": token,
        "user": user
    }

@router.get("/me", response_model=UserOut)
def me(current_user = Depends(get_current_user)):
    return current_user

@router.post("/me/avatar")
async def upload_avatar(
    file: UploadFile,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    user = db.query(User).filter(User.id == current_user.id).first()
    
    if user.avatar_public_id:
        cloudinary.uploader.destroy(user.avatar_public_id)
    
    result = await upload_to_cloudinary(file, folder="avatars")
    
    user.avatar_url = result["secure_url"]
    user.avatar_public_id = result["public_id"]
    
    db.commit()
    db.refresh(user)
    
    return {"avatar_url": user.avatar_url}
@router.delete("/auth/me", status_code=status.HTTP_204_NO_CONTENT)
def delete_own_account(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    delete_user(db, current_user.id)
    return {"detail": "Account deleted successfully"}
