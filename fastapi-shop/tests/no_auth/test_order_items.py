def test_get_order_item_fail(client):
    response = client.get(f"/order_items/1")
    data = response.json()
    
    assert response.status_code == 401
    assert data['detail'] == 'Token not found'

def test_get_order_items_fail(client):
    response = client.get(f"/order_items/")
    data = response.json()
    
    assert response.status_code == 401
    assert data['detail'] == 'Token not found'

def test_update_order_item_fail(client):
    response = client.put(f"/order_items/1", json = 
                        {
                            "products_count": 2,
                            "order_id": 1,
                            "product_id": 1
                        })
    data = response.json()

    assert response.status_code == 401
    assert data['detail'] == 'Token not found'

def test_delete_order_item_fail(client):
    response = client.delete(f"/order_items/1")
    data = response.json()

    assert response.status_code == 401
    assert data['detail'] == 'Token not found'