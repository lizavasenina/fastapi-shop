def test_get_user_fail(client):
    response = client.get(f"/users/1")
    data = response.json()
    
    assert response.status_code == 401
    assert data['detail'] == 'Token not found'

def test_get_users_fail(client):
    response = client.get(f"/users/")
    data = response.json()
    
    assert response.status_code == 401
    assert data['detail'] == 'Token not found'

def test_update_user_fail(client):
    response = client.put(f"/users/1", json = 
                        {
                        "user_name": "new_user",
                        "birth_date": "2000-05-23",
                        "sex": False
                        })
    data = response.json()

    assert response.status_code == 401
    assert data['detail'] == 'Token not found'

def test_delete_user_fail(client):
    response = client.delete(f"/users/1")
    data = response.json()

    assert response.status_code == 401
    assert data['detail'] == 'Token not found'