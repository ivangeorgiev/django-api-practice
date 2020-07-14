import pytest

def test_can_read_api_root(client):
    response = client.get('/api/')
    assert response.status_code == 200

@pytest.mark.django_db
def test_get_usrers_on_empty_db_returns_empty_list(client):
    response = client.get('/api/users/')
    assert response.status_code == 200
    assert isinstance(response.data['results'], list)
    assert [] == response.data['results']

@pytest.mark.django_db
def test_get_usrers_returns_empty_list_of_users(client, test_db):
    response = client.get('/api/users/')
    assert response.status_code == 200
    assert isinstance(response.data['results'], list)
    assert 1 == len(response.data['results'])
    actual = response.data['results'][0]
    assert 'ivang' == actual['username']

@pytest.mark.django_db
def test_read_existing_user_returns_user_info(client, test_db):
    response = client.get('/api/users/1/')
    assert response.status_code == 200
    assert response.data['username'] == 'ivang'
    assert response.data['email'] == 'ivan.georgiev@mail.com'

@pytest.mark.django_db
def test_read_not_existing_user_returns_404(client, test_db):
    response = client.get('/api/users/101/')
    assert response.status_code == 404

@pytest.mark.django_db
def test_put_user_creates_user(client, test_db):
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

