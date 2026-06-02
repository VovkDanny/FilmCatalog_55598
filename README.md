# Katalog Filmów z Ocenami Użytkowników

Kompletna aplikacja webowa napisana w **FastAPI** z systemem ocen, uwierzytelnianiem **JWT**, kontrolą dostępu na podstawie ról (**user / moderator**), testami jednostkowymi oraz konteneryzacją **Docker**.

## Struktura Projektu

```text
movie_catalog/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── crud.py
│   ├── auth.py
│   ├── dependencies.py
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── movies.py
│   │   ├── ratings.py
│   │   └── users.py
│   └── tests/
│       ├── __init__.py
│       ├── conftest.py
│       ├── test_movies.py
│       ├── test_ratings.py
│       └── test_auth.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .env.example
└── README.md
```

---

## Wymagania wstępne

- Python 3.10 lub nowszy
- Docker & Docker Compose (opcjonalnie, do konteneryzacji)

---

## Instrukcja Uruchomienia Lokalnego

1. **Przejdź do katalogu projektu:**
   ```bash
   cd movie_catalog
   ```

2. **Utwórz i aktywuj środowisko wirtualne:**
   ```bash
   python -m venv venv
   # Na Windows:
   venv\Scripts\activate
   # Na macOS/Linux:
   source venv/bin/activate
   ```

3. **Zainstaluj wymagane pakiety:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Skopiuj i uzupełnij zmienne środowiskowe:**
   ```bash
   cp .env.example .env
   ```

5. **Uruchom serwer deweloperski uvicorn:**
   ```bash
   uvicorn app.main:app --reload
   ```

Aplikacja będzie dostępna pod adresem: [http://127.0.0.1:8000](http://127.0.0.1:8000).  
Automatyczna interaktywna dokumentacja Swagger UI znajduje się pod adresem: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

---

## Uruchomienie za pomocą Docker Compose (PostgreSQL)

Docker compose uruchamia dwie powiązane usługi: aplikację FastAPI (`api`) oraz bazę danych PostgreSQL (`db`).

1. **Uruchom kontenery:**
   ```bash
   docker-compose up --build
   ```

2. **Zatrzymaj kontenery:**
   ```bash
   docker-compose down
   ```

Aplikacja automatycznie przeprowadzi migrację i połączy się z kontenerem bazy PostgreSQL.

---

## Testy Jednostkowe

Testy wykorzystują bazę danych SQLite typu in-memory w celu zachowania pełnej izolacji stanów.

Aby uruchomić testy jednostkowe, wykonaj komendę w głównym katalogu projektu:
```bash
python -m pytest
```

---

## Instrukcja Wdrożenia na Railway / Render

### Railway:
1. Załóż konto i zaloguj się na [Railway.app](https://railway.app).
2. Połącz swoje konto z GitHubem i wybierz repozytorium z projektem `movie_catalog`.
3. Railway automatycznie wykryje `Dockerfile` i rozpocznie budowanie obrazu.
4. W zakładce **Variables** dodaj zmienne środowiskowe z pliku `.env.example`:
   - `SECRET_KEY` (silny ciąg znaków)
   - `ALGORITHM` (np. `HS256`)
   - `ACCESS_TOKEN_EXPIRE_MINUTES` (np. `60`)
5. Utwórz nową usługę bazy danych (PostgreSQL) bezpośrednio w projekcie na Railway.
6. Pobierz jej zmienną `DATABASE_URL` i przypisz ją do zmiennej środowiskowej swojej aplikacji `api`.

### Render:
1. Zaloguj się na [Render.com](https://render.com).
2. Wybierz **New** -> **Web Service**.
3. Połącz konto z GitHub i wskaż swoje repozytorium.
4. Ustaw parametry środowiska:
   - **Environment**: `Docker` (Render automatycznie znajdzie `Dockerfile` w głównym katalogu)
5. W sekcji **Advanced** dodaj zmienne środowiskowe:
   - `SECRET_KEY`, `ALGORITHM`, `ACCESS_TOKEN_EXPIRE_MINUTES`.
6. Stwórz na Renderze osobną instancję **Render PostgreSQL**, a następnie skopiuj jej **Internal Database URL** i dodaj do zmiennych Web Service jako `DATABASE_URL`.
7. Zapisz i kliknij **Deploy**.
