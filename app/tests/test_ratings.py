def test_rating_average_and_moderator_delete(client):
    client.post("/register", json={"username": "moderator", "password": "password123"})
    login_mod = client.post("/login", data={"username": "moderator", "password": "password123"})
    mod_token = login_mod.json()["access_token"]
    headers_mod = {"Authorization": f"Bearer {mod_token}"}

    movie_resp = client.post(
        "/movies",
        json={"title": "Interstellar", "year": 2014, "director": "Nolan", "genre": "Sci-Fi"},
        headers=headers_mod
    )
    assert movie_resp.status_code == 201
    movie_id = movie_resp.json()["id"]

    client.post("/register", json={"username": "user1", "password": "password123"})
    client.post("/register", json={"username": "user2", "password": "password123"})

    login_u1 = client.post("/login", data={"username": "user1", "password": "password123"})
    login_u2 = client.post("/login", data={"username": "user2", "password": "password123"})

    token_u1 = login_u1.json()["access_token"]
    token_u2 = login_u2.json()["access_token"]

    headers_u1 = {"Authorization": f"Bearer {token_u1}"}
    headers_u2 = {"Authorization": f"Bearer {token_u2}"}

    r1 = client.post(f"/movies/{movie_id}/rate", json={"rating": 8, "comment": "Super"}, headers=headers_u1).json()
    r2 = client.post(f"/movies/{movie_id}/rate", json={"rating": 10, "comment": "Genialny!"}, headers=headers_u2).json()

    movie_details = client.get(f"/movies/{movie_id}").json()
    assert movie_details["avg_rating"] == 9.0
    assert len(movie_details["ratings"]) == 2

    filter_resp = client.get("/movies?min_rating=8.5").json()
    filter_titles = [m["title"] for m in filter_resp]
    assert "Interstellar" in filter_titles

    filter_resp_high = client.get("/movies?min_rating=9.5").json()
    filter_titles_high = [m["title"] for m in filter_resp_high]
    assert "Interstellar" not in filter_titles_high

    rating_id_u1 = r1["id"]
    delete_fail = client.delete(f"/ratings/{rating_id_u1}", headers=headers_u2)
    assert delete_fail.status_code == 403

    delete_success = client.delete(f"/ratings/{rating_id_u1}", headers=headers_mod)
    assert delete_success.status_code == 200

    movie_details_after = client.get(f"/movies/{movie_id}").json()
    assert movie_details_after["avg_rating"] == 10.0
    assert len(movie_details_after["ratings"]) == 1
