from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import schemas, crud, models
from app.database import get_db
from app.dependencies import get_current_user

router = APIRouter(prefix="/ratings", tags=["Ratings"])

@router.delete("/{rating_id}", response_model=schemas.Rating, summary="Usuń ocenę (Właściciel lub Moderator)")
def delete_rating(
    rating_id: int,
    db: Session = Depends(get_db),
    current_user: models.UserDB = Depends(get_current_user)
):
    """
    Usuwa ocenę o podanym ID.
    - Zwykły użytkownik może usunąć wyłącznie swoją własną ocenę.
    - Moderator może usunąć dowolną ocenę.
    """
    db_rating = crud.get_rating(db, rating_id)
    if not db_rating:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ocena o podanym ID nie została znaleziona"
        )
        
    if current_user.role != "moderator" and db_rating.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Brak uprawnień do usunięcia tej oceny"
        )
        
    return crud.delete_rating(db, rating_id)
