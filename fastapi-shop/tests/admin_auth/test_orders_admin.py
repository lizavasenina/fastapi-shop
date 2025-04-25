def test_get_existent_order_success(client, create_order):
    order_id = create_order['order_id']

    response = client.get(f"/orders/{order_id}")
    data = response.json()
    
    assert response.status_code == 200
    assert data['user_id'] == create_order['user_id']
    assert data['status'] == create_order['status']
    assert data['priority'] == create_order['priority']

def test_get_nonexistent_order_fail(client, create_order):
    order_id = create_order['order_id']
    client.delete(f"/orders/{order_id}")
    
    response = client.get(f"/orders/{order_id}")
    data = response.json()
    
    assert response.status_code == 404
    assert data['detail'] == f'No order with this id: {order_id} found'

def test_create_order_success(client):
    response = client.post("/orders/")
    data = response.json()

    assert response.status_code == 201
    assert data['user_id'] == 1
    assert 'order_id' in data

def test_add_order_valid_user_success(client, create_user):
    user_id = create_user['user_id']
    response = client.post(f"/orders/{user_id}")
    data = response.json()

    assert response.status_code == 201
    assert data['user_id'] == user_id
    assert 'order_id' in data
    
def test_add_order_invalid_user_fail(client, create_user):
    user_id = create_user['user_id']
    client.delete(f"/users/{user_id}")
    response = client.post(f"/orders/{user_id}")
    data = response.json()

    assert response.status_code == 404
    assert data['detail'] == f'No user with this id: {user_id} found'

def test_update_existent_order_valid_user_success(client, create_order, create_user):
    order_id = create_order['order_id']
    user = client.post("/auth/register/", json=
                        {
                            "email": "user2@mail.ru",
                            "password": "123456",
                            "user_name": "user2",
                            "birth_date": "2001-04-23",
                            "sex": True
                        }).json()
    user_id = user['user_id']
    
    try:
        response = client.put(f"/orders/{order_id}", json = 
                                {
                                    "order_date": "2025-04-15",
                                    "priority": 2,
                                    "status": False,
                                    "user_id": user_id
                                })
        data = response.json()

        assert response.status_code == 200
        assert data['user_id'] == user_id
    finally:
        client.delete(f"/users/{user_id}")

def test_update_existent_order_invalid_user_fail(client, create_order):
    order_id = create_order['order_id']
    user = client.post("/auth/register/", json=
                        {
                            "email": "user2@mail.ru",
                            "password": "123456",
                            "user_name": "user2",
                            "birth_date": "2001-04-23",
                            "sex": True
                        }).json()
    user_id = user['user_id']
    client.delete(f"/users/{user_id}")
    
    response = client.put(f"/orders/{order_id}", json = 
                                {
                                    "order_date": "2025-04-15",
                                    "priority": 2,
                                    "status": False,
                                    "user_id": user_id
                                })
    data = response.json()
    
    assert response.status_code == 404
    assert data['detail'] == f'No user with this id: {user_id} found'

def test_update_nonexistent_order_fail(client, create_order):
    order_id = create_order['order_id']
    client.delete(f"/orders/{order_id}")
    
    response = client.put(f"/orders/{order_id}", json = 
                                {
                                    "order_date": "2025-04-15",
                                    "priority": 2,
                                    "status": False,
                                    "user_id": 1
                                })
    data = response.json()
    
    assert response.status_code == 404
    assert data['detail'] == f'No order with this id: {order_id} found'
    
def test_delete_existent_order_success(client, create_order):
    order_id = create_order['order_id']
    
    response = client.delete(f"/orders/{order_id}")
    data = response.json()

    assert response.status_code == 200
    assert data['message'] == f'Order with id {order_id} deleted successfully'

def test_delete_nonexistent_order_fail(client, create_order):
    order_id = create_order['order_id']
    client.delete(f"/orders/{order_id}")
    
    response = client.delete(f"/orders/{order_id}")
    data = response.json()
    
    assert response.status_code == 404
    assert data['detail'] == f'No order with this id: {order_id} found'