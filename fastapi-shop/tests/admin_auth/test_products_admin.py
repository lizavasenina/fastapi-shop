def test_get_existent_product_success(client, create_product):
    product_id = create_product['product_id']

    response = client.get(f"/products/{product_id}")
    data = response.json()
    
    assert response.status_code == 200
    assert data['product_name'] == create_product['product_name']
    assert data['length'] == create_product['length']
    assert data['width'] == create_product['width']
    assert data['height'] == create_product['height']
    assert data['weight'] == create_product['weight']
    assert data['price'] == create_product['price']
    assert data['stock'] == create_product['stock']
    assert data['category_id'] == create_product['category_id']

def test_get_nonexistent_product_fail(client, create_product):
    product_id = create_product['product_id']
    client.delete(f"/products/{product_id}")
    
    response = client.get(f"/products/{product_id}")
    data = response.json()
    
    assert response.status_code == 404
    assert data['detail'] == f'No product with this id: {product_id} found'

def test_create_product_success(client, create_category):
    response = client.post("/products/", json=
                            {
                            "product_name": "product",
                            "length": 0,
                            "width": 0,
                            "height": 0,
                            "weight": 0,
                            "price": 0,
                            "stock": 0,
                            "category_id": create_category['category_id']
                            })
    data = response.json()

    assert response.status_code == 201
    assert data['product_name'] == "product"
    assert 'product_id' in data

def test_update_existent_product_valid_category_success(client, create_product):
    product_id = create_product['product_id']
    category = client.post("/categories/", json={"category_name": "category"}).json()
    category_id = category['category_id']
    
    try:
        response = client.put(f"/products/{product_id}", json = 
                                {
                                "product_name": "product_new",
                                "length": 1,
                                "width": 1,
                                "height": 1,
                                "weight": 1,
                                "price": 1,
                                "stock": 1,
                                "category_id": category_id
                                })
        data = response.json()

        assert response.status_code == 200
        assert data['category_id'] == category_id
    finally:
        client.delete(f"/categories/{category_id}")
    
def test_update_existent_product_invalid_category_fail(client, create_product):
    product_id = create_product['product_id']
    category = client.post("/categories/", json={"category_name": "category"}).json()
    category_id = category['category_id']
    client.delete(f"/categories/{category_id}")
    
    response = client.put(f"/products/{product_id}", json = 
                            {
                            "product_name": "product_new",
                            "length": 1,
                            "width": 1,
                            "height": 1,
                            "weight": 1,
                            "price": 1,
                            "stock": 1,
                            "category_id": category_id
                            })
    data = response.json()

    assert response.status_code == 404
    assert data['detail'] ==  f'No category with this id: {category_id} found'

def test_update_nonexistent_product_fail(client, create_product):
    product_id = create_product['product_id']
    client.delete(f"/products/{product_id}")
    
    response = client.put(f"/products/{product_id}", json = 
                            {
                            "product_name": "product",
                            "length": 0,
                            "width": 0,
                            "height": 0,
                            "weight": 0,
                            "price": 0,
                            "stock": 0,
                            "category_id": 1
                            })
    data = response.json()
    
    assert response.status_code == 404
    assert data['detail'] == f'No product with this id: {product_id} found'

def test_delete_existent_product_success(client, create_product):
    product_id = create_product['product_id']
    
    response = client.delete(f"/products/{product_id}")
    data = response.json()

    assert response.status_code == 200
    assert data['message'] == f'Product with id {product_id} deleted successfully'

def test_delete_nonexistent_product_fail(client, create_product):
    product_id = create_product['product_id']
    client.delete(f"/products/{product_id}")
    
    response = client.delete(f"/products/{product_id}")
    data = response.json()
    
    assert response.status_code == 404
    assert data['detail'] == f'No product with this id: {product_id} found'

def test_increase_stock_valid_quantity_success(client, create_product):
    product_id = create_product['product_id']
    
    response = client.patch(f"/products/{product_id}?quantity=10")
    data = response.json()
    
    assert response.status_code == 200
    assert data['stock'] == 12

def test_increase_stock_invalid_quantity_fail(client, create_product):
    response = client.patch(f"/products/{create_product['product_id']}?quantity=-10")
    data = response.json()
    
    assert response.status_code == 400
    assert data['detail'] == "Product stock cannot be less than 0: -8"