FROM python:3.11-slim

WORKDIR /workspace

# Instalacja zależności systemowych niezbędnych do kompilacji niektórych bibliotek (np. psycopg2)
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Kopiowanie i instalacja wymagań
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Kopiowanie kodu źródłowego
COPY . .

# Otwarcie portu 8000
EXPOSE 8000

# Uruchomienie aplikacji za pomocą uvicorn (z obsługą dynamicznego portu PORT, domyślnie 8000)
CMD uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}

