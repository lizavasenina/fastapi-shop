def test_get_existent_order_item_success(client, create_order_item):
    order_item_id = create_order_item['order_item_id']

    response = client.get(f"/order_items/{order_item_id}")
    data = response.json()
    
    assert response.status_code == 200
    assert data['order_id'] == create_order_item['order_id']
    assert data['products_count'] == create_order_item['products_count']
    assert data['product_id'] == create_order_item['product_id']

def test_get_order_items_success(client, create_order_item):
    response = client.get(f"/order_items/")
    data = response.json()
    
    assert response.status_code == 200
    assert len(data) == 1
    assert isinstance(data, list)
    assert data[0]['order_id'] == create_order_item['order_id']

def test_create_order_item_valid_order_and_product_success(client, create_order):
    order_id = create_order['order_id']
    product_id = 1
    
    response = client.post("/order_items/", json=
                            {
                                "products_count": 1,
                                "order_id": create_order['order_id'],
                                "product_id": product_id
                            })
    data = response.json()

    assert response.status_code == 201
    assert data['order_id'] == order_id
    assert data['product_id'] == product_id
    assert 'order_item_id' in data

def test_update_existent_order_item_valid_product_count_success(client, create_order_item, create_order):
    order_item_id = create_order_item['order_item_id']
    product_id = 1
    
    response = client.put(f"/order_items/{order_item_id}", json=
                        {
                            "products_count": 2,
                            "order_id": create_order['order_id'],
                            "product_id": product_id
                        })
        
    assert response.status_code == 200

def test_delete_order_item_success(client, create_order_item):
    order_item_id = create_order_item['order_item_id']
    
    response = client.delete(f"/order_items/{order_item_id}")
    data = response.json()

    assert response.status_code == 200
    assert data['message'] == f'OrderItem with id {order_item_id} deleted successfully'
