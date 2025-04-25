def test_get_existent_user_success(client, authenticate_user):
    user_id = authenticate_user['user_id']

    response = client.get(f"/users/{user_id}")
    data = response.json()
    
    assert response.status_code == 200
    assert data['user_name'] == authenticate_user['user_name']

def test_get_other_user_fail(client):
    response = client.get(f"/users/1")
    data = response.json()
    
    assert response.status_code == 403
    assert data['detail'] == 'No access'

def test_get_users_fail(client):
    response = client.get(f"/users/")
    data = response.json()
    
    assert response.status_code == 403
    assert data['detail'] == 'The user is not admin'

def test_update_user_success(client, authenticate_user):
    user_id = authenticate_user['user_id']
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

def test_update_other_user_fail(client):
    response = client.put(f"/users/1")
    data = response.json()
    
    assert response.status_code == 403
    assert data['detail'] == 'No access'