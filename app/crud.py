from sqlalchemy.orm import Session, joinedload
from app import models, schemas, auth

def get_movies(db: Session, genre: str = None, min_rating: float = None, skip: int = 0, limit: int = 10):
    query = db.query(models.MovieDB)
    if genre:
        query = query.filter(models.MovieDB.genre.ilike(genre))
    
    movies = query.all()
    if min_rating is not None:
        movies = [m for m in movies if m.avg_rating is not None and m.avg_rating >= min_rating]
        
    return movies[skip : skip + limit]

def get_movie(db: Session, movie_id: int):
    return db.query(models.MovieDB).filter(models.MovieDB.id == movie_id).first()

def create_movie(db: Session, movie: schemas.MovieCreate):
    db_movie = models.MovieDB(
        title=movie.title,
        year=movie.year,
        director=movie.director,
        genre=movie.genre
    )
    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)
    return db_movie

def update_movie(db: Session, movie_id: int, movie: schemas.MovieCreate):
    db_movie = get_movie(db, movie_id)
    if not db_movie:
        return None
    db_movie.title = movie.title
    db_movie.year = movie.year
    db_movie.director = movie.director
    db_movie.genre = movie.genre
    db.commit()
    db.refresh(db_movie)
    return db_movie

def delete_movie(db: Session, movie_id: int):
    db_movie = get_movie(db, movie_id)
    if not db_movie:
        return None
    db.delete(db_movie)
    db.commit()
    return db_movie

def get_user_by_username(db: Session, username: str):
    return db.query(models.UserDB).filter(models.UserDB.username == username).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_pwd = auth.get_password_hash(user.password)
    role = "moderator" if user.username.lower() in ["moderator", "admin"] else "user"
    
    db_user = models.UserDB(
        username=user.username,
        hashed_password=hashed_pwd,
        role=role
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_rating(db: Session, rating_id: int):
    return db.query(models.RatingDB).options(joinedload(models.RatingDB.user)).filter(models.RatingDB.id == rating_id).first()

def create_or_update_rating(db: Session, rating_in: schemas.RatingCreate, movie_id: int, user_id: int):
    db_rating = db.query(models.RatingDB).filter(
        models.RatingDB.movie_id == movie_id,
        models.RatingDB.user_id == user_id
    ).first()
    
    if db_rating:
        db_rating.rating = rating_in.rating
        db_rating.comment = rating_in.comment
    else:
        db_rating = models.RatingDB(
            rating=rating_in.rating,
            comment=rating_in.comment,
            movie_id=movie_id,
            user_id=user_id
        )
        db.add(db_rating)
        
    db.commit()
    db.refresh(db_rating)
    return db_rating

def delete_rating(db: Session, rating_id: int):
    db_rating = get_rating(db, rating_id)
    if not db_rating:
        return None
    db.delete(db_rating)
    db.commit()
    return db_rating
