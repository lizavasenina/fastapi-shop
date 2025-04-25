import pytest
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture(scope="module")
def client():
    yield TestClient(app)

@pytest.fixture(scope='module', autouse=True)
def authenticate_user(client : TestClient):
    user = client.post("/auth/register/", json=
                        {"email": "user@mail.ru",
                        "password": "1234",
                        "user_name": "user",
                        "birth_date": "2000-04-23",
                        "sex": True
                        }).json()
    client.post("/auth/login/", json={"email": "user@mail.ru", "password": "1234"})
    yield user
    client.delete(f"/users/{user['user_id']}")
    client.post("/auth/logout/")

@pytest.fixture()
def create_order(client):
    order = client.post(f"/orders/").json()
    yield order
    client.delete(f"/orders/{order['order_id']}")

@pytest.fixture()
def create_order_item(client, create_order):
    order_item = client.post(f"/order_items/", json=
                                {
                                    "products_count": 1,
                                    "order_id": create_order['order_id'],
                                    "product_id": 1
                                }).json()
    yield order_item
    client.delete(f"/orders/{order_item['order_id']}")