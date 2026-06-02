from fastapi import FastAPI
import json
from pathlib import Path
from app import models
from app.database import engine, get_db
from app.routers import movies, ratings, users

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Katalog filmów z ocenami użytkowników",
    description="Kompletna aplikacja webowa w FastAPI z ocenami, uwierzytelnianiem JWT i podziałem ról.",
    version="1.0.0"
)

@app.get("/health", tags=["General"]) 
async def health():
    return {"status": "OK"}

def populate_db():
    db = next(get_db())
    try:
        if db.query(models.MovieDB).count() == 0:
            json_path = Path(__file__).parent / "movies.json"
            if json_path.exists():
                with open(json_path, "r", encoding="utf-8") as f:
                    movies = json.load(f)
                    for m in movies:
                        db_movie = models.MovieDB(
                            title=m.get("title"),
                            year=m.get("year"),
                            director=m.get("director"),
                            genre=m.get("genre")
                        )
                        db.add(db_movie)
                    db.commit()
    except Exception:
        db.rollback()
    finally:
        db.close()

populate_db()

app.include_router(users.router)
app.include_router(movies.router)
app.include_router(ratings.router)

@app.get("/", tags=["General"])
def read_root():
    return {
        "message": "Witaj w Katalogu Filmów z ocenami użytkowników!",
        "documentation": "/docs"
    }
