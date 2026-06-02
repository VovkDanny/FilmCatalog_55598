def test_create_movie_permissions(client):
    response = client.post(
        "/movies",
        json={"title": "Interstellar", "year": 2014, "director": "Christopher Nolan", "genre": "Sci-Fi"}
    )
    assert response.status_code == 401

    client.post("/register", json={"username": "normaluser", "password": "password123"})
    login_user = client.post("/login", data={"username": "normaluser", "password": "password123"})
    user_token = login_user.json()["access_token"]
    
    headers = {"Authorization": f"Bearer {user_token}"}
    response_user = client.post(
        "/movies",
        json={"title": "Interstellar", "year": 2014, "director": "Christopher Nolan", "genre": "Sci-Fi"},
        headers=headers
    )
    assert response_user.status_code == 403

def test_movies_filtering_and_pagination(client):
    client.post("/register", json={"username": "moderator", "password": "password123"})
    login_mod = client.post("/login", data={"username": "moderator", "password": "password123"})
    mod_token = login_mod.json()["access_token"]
    headers = {"Authorization": f"Bearer {mod_token}"}
    
    client.post("/movies", json={"title": "Inception", "year": 2010, "director": "Nolan", "genre": "Sci-Fi"}, headers=headers)
    client.post("/movies", json={"title": "Pulp Fiction", "year": 1994, "director": "Tarantino", "genre": "Crime"}, headers=headers)
    
    response = client.get("/movies")
    assert response.status_code == 200
    movies = response.json()
    titles = [m["title"] for m in movies]
    assert "Inception" in titles
    assert "Pulp Fiction" in titles

    response_genre = client.get("/movies?genre=Sci-Fi")
    movies_genre = response_genre.json()
    assert len(movies_genre) >= 1
    assert any(m["title"] == "Inception" for m in movies_genre)
    assert all(m["genre"] == "Sci-Fi" for m in movies_genre)
