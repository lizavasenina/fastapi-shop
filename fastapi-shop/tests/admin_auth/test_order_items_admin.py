def test_get_existent_order_item_success(client, create_order_item):
    order_item_id = create_order_item['order_item_id']

    response = client.get(f"/order_items/{order_item_id}")
    data = response.json()
    
    assert response.status_code == 200
    assert data['order_id'] == create_order_item['order_id']
    assert data['products_count'] == create_order_item['products_count']
    assert data['product_id'] == create_order_item['product_id']

def test_get_nonexistent_order_item_fail(client, create_order_item):
    order_item_id = create_order_item['order_item_id']
    client.delete(f"/order_items/{order_item_id}")
    
    response = client.get(f"/order_items/{order_item_id}")
    data = response.json()
    
    assert response.status_code == 404
    assert data['detail'] == f'No order item with this id: {order_item_id} found'

def test_get_existent_order_items_success(client, create_order_item):
    existing = len(client.get(f"/order_items/").json())
    
    response = client.get(f"/order_items/?skip={existing-1}&limit=1")
    data = response.json()
    
    assert response.status_code == 200
    assert len(data) == 1
    assert isinstance(data, list)
    assert data[0]['order_id'] == create_order_item['order_id']

def test_create_order_item_valid_order_and_product_success(client, create_product, create_order):
    order_id = create_order['order_id']
    product_id = create_product['product_id']
    
    response = client.post("/order_items/", json=
                            {
                                "products_count": 1,
                                "order_id": create_order['order_id'],
                                "product_id": create_product['product_id']
                            })
    data = response.json()

    assert response.status_code == 201
    assert data['order_id'] == order_id
    assert data['product_id'] == product_id
    assert 'order_item_id' in data
    
def test_create_order_item_invalid_order_fail(client, create_order, create_product):
    order_id = create_order['order_id']
    client.delete(f"/orders/{order_id}")
    
    response = client.post("/order_items/", json=
                                {
                                    "products_count": 1,
                                    "order_id": order_id,
                                    "product_id": create_product['product_id']
                                })
    data = response.json()

    assert response.status_code == 404
    assert data['detail'] == f'No order with this id: {order_id} found'
    
def test_create_order_item_invalid_product_fail(client, create_order, create_product):
    product_id = create_product['product_id']
    client.delete(f"/products/{product_id}")
    
    response = client.post("/order_items/", json=
                                {
                                    "products_count": 1,
                                    "order_id": create_order['order_id'],
                                    "product_id": product_id
                                })
    data = response.json()

    assert response.status_code == 404
    assert data['detail'] == f'No product with this id: {product_id} found'

def test_create_order_item_invalid_product_count_fail(client, create_order, create_product):
    response = client.post("/order_items/", json=
                                {
                                    "products_count": 10,
                                    "order_id": create_order['order_id'],
                                    "product_id": create_product['product_id']
                                })

    assert response.status_code == 400

def test_update_existent_order_item_valid_product_count_success(client, create_order_item, create_order, create_product):
    order_item_id = create_order_item['order_item_id']
    
    response = client.put(f"/order_items/{order_item_id}", json=
                        {
                            "products_count": 2,
                            "order_id": create_order['order_id'],
                            "product_id": create_product['product_id']
                        })
    product = client.get(f"/products/{create_product['product_id']}").json()
    
    assert response.status_code == 200
    assert product['stock'] == 0

def test_update_existent_order_item_invalid_product_count_fail(client, create_order_item, create_order, create_product):
    order_item_id = create_order_item['order_item_id']
    
    response = client.put(f"/order_items/{order_item_id}", json=
                        {
                            "products_count": 10,
                            "order_id": create_order['order_id'],
                            "product_id": create_product['product_id']
                        })
    data = response.json()
    
    assert response.status_code == 400
    assert data['detail'] == f'The count of products in the order is more than the stock (stock: 2, count: 10)'


def test_update_nonexistent_order_item_fail(client, create_order):
    order_item_id = create_order['order_id']
    client.delete(f"/order_items/{order_item_id}")
    
    response = client.put(f"/order_items/{order_item_id}", json = 
                                {
                                    "products_count": 10,
                                    "order_id": 1,
                                    "product_id": 2
                                })
    data = response.json()
    
    assert response.status_code == 404
    assert data['detail'] == f'No order item with this id: {order_item_id} found'

def test_delete_existent_order_item_success(client, create_order_item):
    order_item_id = create_order_item['order_item_id']
    
    response = client.delete(f"/order_items/{order_item_id}")
    data = response.json()

    assert response.status_code == 200
    assert data['message'] == f'OrderItem with id {order_item_id} deleted successfully'

def test_delete_nonexistent_order_item_fail(client, create_order_item):
    order_item_id = create_order_item['order_item_id']
    client.delete(f"/order_items/{order_item_id}")
    
    response = client.delete(f"/order_items/{order_item_id}")
    data = response.json()
    
    assert response.status_code == 404
    assert data['detail'] == f'No order item with this id: {order_item_id} found'