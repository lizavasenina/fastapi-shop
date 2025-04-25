def test_get_existent_user_success(client, create_user):
    user_id = create_user['user_id']

    response = client.get(f"/users/{user_id}")
    data = response.json()
    
    assert response.status_code == 200
    assert data['user_name'] == create_user['user_name']

def test_get_nonexistent_user_fail(client, create_user):
    user_id = create_user['user_id']
    client.delete(f"/users/{user_id}")
    
    response = client.get(f"/users/{user_id}")
    data = response.json()
    
    assert response.status_code == 404
    assert data['detail'] == f'No user with this id: {user_id} found'

def test_get_existent_users_success(client, create_user):
    existing = len(client.get(f"/users/").json())
    
    response = client.get(f"/users/?skip={existing-1}&limit=1")
    data = response.json()
    
    assert response.status_code == 200
    assert len(data) == 1
    assert isinstance(data, list)
    assert data[0]['user_name'] == create_user['user_name']

def test_update_existent_user_success(client, create_user):
    user_id = create_user['user_id']
    new_user_name = "user_new"
    
    response = client.put(f"/users/{user_id}", json = 
                        {
                        "user_name": f"{new_user_name}",
                        "birth_date": "2000-05-23",
                        "sex": False
                        })
    data = response.json()

    assert response.status_code == 200
    assert data['user_name'] == new_user_name

def test_update_nonexistent_user_fail(client, create_user):
    user_id = create_user['user_id']
    client.delete(f"/users/{user_id}")
    new_user_name = "user_new"
    
    response = client.put(f"/users/{user_id}", json = 
                    {
                    "user_name": f"{new_user_name}",
                    "birth_date": "2000-05-23",
                    "sex": False
                    })
    data = response.json()
    
    assert response.status_code == 404
    assert data['detail'] == f'No user with this id: {user_id} found'

def test_delete_existent_user_success(client, create_user):
    user_id = create_user['user_id']
    
    response = client.delete(f"/users/{user_id}")
    data = response.json()

    assert response.status_code == 200
    assert data['message'] == f'User with id {user_id} deleted successfully'

def test_delete_nonexistent_user_fail(client, create_user):
    user_id = create_user['user_id']
    client.delete(f"/users/{user_id}")
    
    response = client.delete(f"/users/{user_id}")
    data = response.json()
    
    assert response.status_code == 404
    assert data['detail'] == f'No user with this id: {user_id} found'