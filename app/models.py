from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class MovieDB(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    year = Column(Integer, nullable=False)
    director = Column(String, nullable=False)
    genre = Column(String, nullable=False)

    ratings = relationship("RatingDB", back_populates="movie", cascade="all, delete-orphan")

    @property
    def avg_rating(self) -> float | None:
        if not self.ratings:
            return None
        ratings_sum = sum(r.rating for r in self.ratings)
        return round(ratings_sum / len(self.ratings), 2)

class UserDB(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, default="user", nullable=False)

    ratings = relationship("RatingDB", back_populates="user", cascade="all, delete-orphan")

class RatingDB(Base):
    __tablename__ = "ratings"

    id = Column(Integer, primary_key=True, index=True)
    rating = Column(Integer, nullable=False)
    comment = Column(String, nullable=True)
    
    movie_id = Column(Integer, ForeignKey("movies.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    movie = relationship("MovieDB", back_populates="ratings")
    user = relationship("UserDB", back_populates="ratings")

    @property
    def username(self) -> str:
        return self.user.username if self.user else ""
