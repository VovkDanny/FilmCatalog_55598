from pydantic import BaseModel, Field
from typing import List, Optional

class RatingBase(BaseModel):
    rating: int = Field(..., ge=1, le=10, description="Ocena filmu w skali od 1 do 10")
    comment: Optional[str] = Field(None, description="Opcjonalny komentarz do oceny")

class RatingCreate(RatingBase):
    pass

class Rating(RatingBase):
    id: int
    movie_id: int
    user_id: int
    username: str

    class Config:
        from_attributes = True

class MovieBase(BaseModel):
    title: str = Field(..., min_length=1, description="Tytuł filmu (minimum 1 znak)")
    year: int = Field(..., ge=1888, le=2026, description="Rok produkcji (między 1888 a 2026)")
    director: str = Field(..., min_length=1, description="Reżyser filmu")
    genre: str = Field(..., min_length=1, description="Gatunek filmu")

class MovieCreate(MovieBase):
    pass

class Movie(MovieBase):
    id: int
    avg_rating: Optional[float] = Field(None, description="Średnia ocena filmu (obliczana automatycznie)")
    ratings: List[Rating] = Field(default=[], description="Lista ocen przypisanych do filmu")

    class Config:
        from_attributes = True

class UserBase(BaseModel):
    username: str = Field(..., min_length=3, description="Nazwa użytkownika (minimum 3 znaki)")

class UserCreate(UserBase):
    password: str = Field(..., min_length=6, description="Hasło użytkownika (minimum 6 znaków)")

class User(UserBase):
    id: int
    role: str

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
    role: Optional[str] = None
