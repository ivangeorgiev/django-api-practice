import pytest
import requests

def test_can_read_api_root(empty_db, client):
    response = client.get('/api/')
    assert response.status_code == 200

def test_get_usrers_on_empty_db_returns_empty_list(empty_db, client):
    response = client.get('/api/users/')
    assert response.status_code == 200
    assert isinstance(response.data['results'], list)
    assert [] == response.data['results']

def test_get_usrers_returns_empty_list_of_users(client, test_db):
    response = client.get('/api/users/')
    assert response.status_code == 200
    assert isinstance(response.data['results'], list)
    assert 1 == len(response.data['results'])
    actual = response.data['results'][0]
    assert 'ivang' == actual['username']

def test_read_existing_user_returns_user_info(client, test_db):
    response = client.get('/api/users/1/')
    assert response.status_code == 200
    assert response.data['username'] == 'ivang'
    assert response.data['email'] == 'ivan.georgiev@mail.com'

def test_read_not_existing_user_returns_404(client, test_db):
    response = client.get('/api/users/101/')
    assert response.status_code == 404

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

# @pytest.mark.skip('Failing because of zscaler')
def test_get_user_from_live_server_returns_user(live_server, test_db):
    url = '{}/api/users/1/'.format(live_server.url)
    response = requests.get(url)
    print(response.text)
    assert response.status_code == 200
    actual = response.json()
    assert 'ivang' == actual['username']
