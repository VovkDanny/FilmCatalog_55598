from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app import schemas, crud, auth
from app.database import get_db

router = APIRouter(tags=["Users / Authentication"])

@router.post("/register", response_model=schemas.User, status_code=status.HTTP_201_CREATED, summary="Zarejestruj nowego użytkownika")
def register(user_in: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    Rejestruje nowego użytkownika w bazie danych. 
    Dla użytkowników o nazwie 'admin' lub 'moderator' automatycznie przypisywana jest rola 'moderator'.
    """
    db_user = crud.get_user_by_username(db, user_in.username)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Użytkownik o podanej nazwie już istnieje"
        )
    return crud.create_user(db, user_in)

@router.post("/login", response_model=schemas.Token, summary="Zaloguj się po token JWT")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Uwierzytelnia użytkownika na podstawie nazwy użytkownika i hasła, a następnie zwraca token JWT.
    Kompatybilne z mechanizmem logowania Swagger UI (Authorize).
    """
    db_user = crud.get_user_by_username(db, form_data.username)
    if not db_user or not auth.verify_password(form_data.password, db_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Niepoprawna nazwa użytkownika lub hasło",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = auth.create_access_token(data={"sub": db_user.username, "role": db_user.role})
    return {"access_token": access_token, "token_type": "bearer"}
