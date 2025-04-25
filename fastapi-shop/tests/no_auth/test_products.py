def test_get_product_success(client):
    response = client.get(f"/products/1")
    assert response.status_code != 401

def test_get_products_success(client):
    response = client.get(f"/products/")
    assert response.status_code != 401

def test_update_product_fail(client):
    response = client.put(f"/products/1")
    data = response.json()

    assert response.status_code == 401
    assert data['detail'] == 'Token not found'

def test_delete_product_fail(client):
    response = client.delete(f"/products/1")
    data = response.json()

    assert response.status_code == 401
    assert data['detail'] == 'Token not found'