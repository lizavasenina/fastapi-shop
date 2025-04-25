def test_get_order_fail(client):
    response = client.get(f"/orders/1")
    data = response.json()
    
    assert response.status_code == 401
    assert data['detail'] == 'Token not found'

def test_get_orders_fail(client):
    response = client.get(f"/orders/")
    data = response.json()
    
    assert response.status_code == 401
    assert data['detail'] == 'Token not found'

def test_update_order_fail(client):
    response = client.put(f"/orders/1", json = 
                        {
                            "order_date": "2025-04-15",
                            "priority": 2,
                            "status": False,
                            "user_id": 1
                        })
    data = response.json()

    assert response.status_code == 401
    assert data['detail'] == 'Token not found'

def test_delete_order_fail(client):
    response = client.delete(f"/orders/1")
    data = response.json()

    assert response.status_code == 401
    assert data['detail'] == 'Token not found'