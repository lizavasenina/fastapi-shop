def test_get_category_success(client):
    response = client.get(f"/categories/1")
    assert response.status_code != 401

def test_get_categories_success(client):
    response = client.get(f"/categories/")
    assert response.status_code != 401

def test_update_category_fail(client):
    response = client.put(f"/categories/1")
    data = response.json()

    assert response.status_code == 401
    assert data['detail'] == 'Token not found'

def test_delete_category_fail(client):
    response = client.delete(f"/categories/1")
    data = response.json()

    assert response.status_code == 401
    assert data['detail'] == 'Token not found'