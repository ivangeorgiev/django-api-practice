import pytest

def test_can_read_api_root(client):
    response = client.get('/api/')
    assert response.status_code == 200


@pytest.mark.django_db
def test_get_user(client, test_db):
    response = client.get('/api/users/1/')
    assert response.status_code == 200
    assert response.data['username'] == 'ivang'

@pytest.mark.django_db
def test_create_user(client, test_db):
    data = {
        'username':'bbeggins',
        'email': 'bbeggins@domain.com',
    }
    response = client.post('/api/users/', data=data)
    print(response.data)
    assert response.status_code == 201
    assert '/api/users/2/' in response.data['url']
    user_response = client.get('/api/users/2/')
    assert user_response.status_code == 200
    assert 'bbeggins' == user_response.data['username']

