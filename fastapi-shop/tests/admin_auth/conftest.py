import pytest
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture(scope="module")
def client():
    yield TestClient(app)

@pytest.fixture(scope="module", autouse=True)
def authenticate(client):
    client.post("/auth/login/", json={"email": "liza_vasenina@mail.ru", "password": "g67j9ksn5"})
    yield
    client.post("/auth/logout/")

@pytest.fixture()
def create_category(client):
    category = client.post("/categories/", json={"category_name": "category"}).json()
    yield category
    client.delete(f"/categories/{category['category_id']}")

@pytest.fixture()
def create_user(client):
    user = client.post("/auth/register/", json=
                        {"email": "user1@mail.ru",
                        "password": "12345",
                        "user_name": "user1",
                        "birth_date": "2000-04-23",
                        "sex": True
                        }).json()
    yield user
    client.delete(f"/users/{user['user_id']}")

@pytest.fixture()
def create_order(client, create_user):
    order = client.post(f"/orders/{create_user['user_id']}").json()
    yield order
    client.delete(f"/orders/{order['order_id']}")

@pytest.fixture()
def create_order_item(client, create_order, create_product):
    order_item = client.post(f"/order_items/", json=
                                {
                                    "products_count": 1,
                                    "order_id": create_order['order_id'],
                                    "product_id": create_product['product_id']
                                }).json()
    yield order_item
    client.delete(f"/orders/{order_item['order_id']}")

@pytest.fixture()
def create_product(client, create_category):
    product = client.post("/products/", json=
        {
        "product_name": "product",
        "length": 2,
        "width": 2,
        "height": 2,
        "weight": 2,
        "price": 2,
        "stock": 2,
        "category_id": create_category['category_id']
        }).json()
    yield product
    client.delete(f"/products/{product['product_id']}")