def test_get_product_success(client):
    response = client.get(f"/products/1")
    assert response.status_code != 403

def test_get_products_success(client):
    response = client.get(f"/products/")
    assert response.status_code != 403

def test_create_product_fail(client):
    response = client.post("/products/")
    data = response.json()

    assert response.status_code == 403
    assert data['detail'] == 'The user is not admin'

def test_update_product_fail(client):
    response = client.put(f"/products/1")
    data = response.json()
    
    assert response.status_code == 403
    assert data['detail'] == 'The user is not admin'

def test_delete_product_fail(client):
    response = client.delete(f"/products/1")
    data = response.json()
    
    assert response.status_code == 403
    assert data['detail'] == 'The user is not admin'