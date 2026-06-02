from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app import schemas, crud, models
from app.database import get_db
from app.dependencies import get_current_user, require_moderator

router = APIRouter(prefix="/movies", tags=["Movies"])

@router.get("", response_model=List[schemas.Movie], summary="Pobierz listę filmów z filtrami i paginacją")
def get_movies(
    genre: Optional[str] = None,
    min_rating: Optional[float] = None,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """
    Zwraca listę filmów z możliwością filtrowania po gatunku (?genre=...) i minimalnej średniej ocenie (?min_rating=...).
    Obsługuje również stronicowanie (?skip=0&limit=10).
    """
    return crud.get_movies(db, genre=genre, min_rating=min_rating, skip=skip, limit=limit)

@router.get("/{movie_id}", response_model=schemas.Movie, summary="Pobierz film po ID")
def get_movie(movie_id: int, db: Session = Depends(get_db)):
    """
    Zwraca pojedynczy film wraz z jego ocenami i średnią oceną.
    """
    db_movie = crud.get_movie(db, movie_id)
    if not db_movie:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Film o podanym ID nie został znaleziony"
        )
    return db_movie

@router.post("", response_model=schemas.Movie, status_code=status.HTTP_201_CREATED, summary="Dodaj nowy film (Tylko Moderator)")
def create_movie(
    movie_in: schemas.MovieCreate,
    db: Session = Depends(get_db),
    current_user: models.UserDB = Depends(require_moderator)
):
    """
    Tworzy nowy film w bazie danych. Wymaga uprawnień moderatora.
    """
    return crud.create_movie(db, movie_in)

@router.put("/{movie_id}", response_model=schemas.Movie, summary="Aktualizuj film (Tylko Moderator)")
def update_movie(
    movie_id: int,
    movie_in: schemas.MovieCreate,
    db: Session = Depends(get_db),
    current_user: models.UserDB = Depends(require_moderator)
):
    """
    Aktualizuje dane filmu o podanym ID. Wymaga uprawnień moderatora.
    """
    db_movie = crud.update_movie(db, movie_id, movie_in)
    if not db_movie:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Film o podanym ID nie został znaleziony"
        )
    return db_movie

@router.delete("/{movie_id}", response_model=schemas.Movie, summary="Usuń film (Tylko Moderator)")
def delete_movie(
    movie_id: int,
    db: Session = Depends(get_db),
    current_user: models.UserDB = Depends(require_moderator)
):
    """
    Usuwa film o podanym ID. Wymaga uprawnień moderatora.
    """
    db_movie = crud.delete_movie(db, movie_id)
    if not db_movie:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Film o podanym ID nie został znaleziony"
        )
    return db_movie

@router.post("/{movie_id}/rate", response_model=schemas.Rating, summary="Oceń film (Zalogowany Użytkownik)")
def rate_movie(
    movie_id: int,
    rating_in: schemas.RatingCreate,
    db: Session = Depends(get_db),
    current_user: models.UserDB = Depends(get_current_user)
):
    """
    Umożliwia zalogowanemu użytkownikowi wystawienie oceny (1-10) wraz z opcjonalnym komentarzem.
    Jeśli użytkownik ocenił już ten film, ocena zostanie zaktualizowana.
    """
    db_movie = crud.get_movie(db, movie_id)
    if not db_movie:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Film o podanym ID nie został znaleziony"
        )
    return crud.create_or_update_rating(db, rating_in, movie_id, current_user.id)
