def test_register(client):
    try:
        response = client.post("/auth/register", json=
                                {
                                    "email": "user@mail.ru",
                                    "password": "1234",
                                    "user_name": "user",
                                    "birth_date": "2000-04-23",
                                    "sex": True
                                })
        data = response.json()
        assert response.status_code == 201
    finally:
        client.post("/auth/login/", json={"email": "user@mail.ru", "password": "1234"})
        client.delete(f"/users/{data['user_id']}")
        client.post("/auth/logout/")

def test_login(client):
    register = client.post("/auth/register", json=
                                {
                                    "email": "user@mail.ru",
                                    "password": "1234",
                                    "user_name": "user",
                                    "birth_date": "2000-04-23",
                                    "sex": True
                                }).json()
    try:
        response = client.post("/auth/login/", json={"email": "user@mail.ru", "password": "1234"})
        data = response.json()
        assert response.status_code == 200
        assert 'access_token' in data
    finally:
        client.delete(f"/users/{register['user_id']}")
        client.post("/auth/logout/")