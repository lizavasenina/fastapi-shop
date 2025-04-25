def test_get_order_success(client, create_order):
    order_id = create_order['order_id']

    response = client.get(f"/orders/{order_id}")
    data = response.json()
    
    assert response.status_code == 200
    assert data['user_id'] == create_order['user_id']
    assert data['status'] == create_order['status']
    assert data['priority'] == create_order['priority']

def test_get_orders_success(client):
    response = client.get(f"/orders/")
    assert response.status_code == 200

def test_create_order_success(client, authenticate_user):
    response = client.post("/orders/")
    data = response.json()

    assert response.status_code == 201
    assert data['user_id'] == authenticate_user['user_id']
    assert 'order_id' in data

def test_add_order_fail(client):
    response = client.post("/orders/1")
    data = response.json()

    assert response.status_code == 403
    assert data['detail'] == 'The user is not admin'

def test_update_order_fail(client, authenticate_user, create_order):
    order_id = create_order['order_id']
    user_id = authenticate_user['user_id']

    response = client.put(f"/orders/{order_id}", json = 
                            {
                                "order_date": "2025-04-15",
                                "priority": 2,
                                "status": False,
                                "user_id": user_id
                            })
    data = response.json()

    assert response.status_code == 403
    assert data['detail'] == 'The user is not admin'

def test_delete_order_success(client, create_order):
    order_id = create_order['order_id']
    
    response = client.delete(f"/orders/{order_id}")
    data = response.json()

    assert response.status_code == 200
    assert data['message'] == f'Order with id {order_id} deleted successfully'
