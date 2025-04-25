def test_get_existent_category_success(client, create_category):
    category_id = create_category['category_id']

    response = client.get(f"/categories/{category_id}")
    data = response.json()
    
    assert response.status_code == 200
    assert data['category_name'] == create_category['category_name']

def test_get_nonexistent_category_fail(client, create_category):
    category_id = create_category['category_id']
    client.delete(f"/categories/{category_id}")
    
    response = client.get(f"/categories/{category_id}")
    data = response.json()
    
    assert response.status_code == 404
    assert data['detail'] == f'No category with this id: {category_id} found'

def test_get_existent_categories_success(client, create_category):
    existing = len(client.get(f"/categories/").json())
    
    response = client.get(f"/categories/?skip={existing-1}&limit=1")
    data = response.json()
    
    assert response.status_code == 200
    assert len(data) == 1
    assert isinstance(data, list)
    assert data[0]['category_name'] == create_category['category_name']

def test_create_category_success(client):
    response = client.post("/categories/", json={"category_name": "category"})
    data = response.json()

    assert response.status_code == 201
    assert data['category_name'] == "category"
    assert 'category_id' in data

def test_update_existent_category_success(client, create_category):
    category_id = create_category['category_id']
    new_category_name = "category_new"
    
    response = client.put(f"/categories/{category_id}", json = {"category_name": f"{new_category_name}"})
    data = response.json()

    assert response.status_code == 200
    assert data['category_name'] == new_category_name

def test_update_nonexistent_category_fail(client, create_category):
    category_id = create_category['category_id']
    client.delete(f"/categories/{category_id}")
    new_category_name = "category_new"
    
    response = client.put(f"/categories/{category_id}", json = {"category_name": f"{new_category_name}"})
    data = response.json()
    
    assert response.status_code == 404
    assert data['detail'] == f'No category with this id: {category_id} found'

def test_delete_existent_category_success(client, create_category):
    category_id = create_category['category_id']
    
    response = client.delete(f"/categories/{category_id}")
    data = response.json()

    assert response.status_code == 200
    assert data['message'] == f'Category with id {category_id} deleted successfully'

def test_delete_nonexistent_category_fail(client, create_category):
    category_id = create_category['category_id']
    client.delete(f"/categories/{category_id}")
    
    response = client.delete(f"/categories/{category_id}")
    data = response.json()
    
    assert response.status_code == 404
    assert data['detail'] == f'No category with this id: {category_id} found'