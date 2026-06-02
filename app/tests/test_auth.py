def test_register_and_login(client):
    register_response = client.post(
        "/register",
        json={"username": "testuser", "password": "password123"}
    )
    assert register_response.status_code == 201
    data = register_response.json()
    assert data["username"] == "testuser"
    assert "id" in data
    assert data["role"] == "user"

    duplicate_response = client.post(
        "/register",
        json={"username": "testuser", "password": "newpassword123"}
    )
    assert duplicate_response.status_code == 400
    assert duplicate_response.json()["detail"] == "Użytkownik o podanej nazwie już istnieje"

    login_response = client.post(
        "/login",
        data={"username": "testuser", "password": "password123"}
    )
    assert login_response.status_code == 200
    login_data = login_response.json()
    assert "access_token" in login_data
    assert login_data["token_type"] == "bearer"

    bad_login_response = client.post(
        "/login",
        data={"username": "testuser", "password": "wrongpassword"}
    )
    assert bad_login_response.status_code == 401
    assert bad_login_response.json()["detail"] == "Niepoprawna nazwa użytkownika lub hasło"
