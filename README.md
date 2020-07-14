# django-api-practice

REST API with Django and Django REST Framework



# Run the project

```bash
$ py -3.7 -m venv .venv
$ source .venv/Scripts/activate
$ python -m pip install --upgrade pip

$ pip install -r requirements.txt
$ python manage.py makemigrations
$ python manage.py migrate

$ python manage.py runserver
```

Open your browser and navigate to http://localhost:8000/api/.

## Run Unit Tests

```bash
$ pytest -vv --cov=rapidapipractice --cov=api --cov-report=term
```



```
(.venv) C:\Sandbox\Learn\Python\Django\django-api-practice>pytest -vv --cov=rapidapipractice --cov=api --cov-report=term
================================================================== test session starts ===================================================================
platform win32 -- Python 3.7.6rc1, pytest-5.4.3, py-1.9.0, pluggy-0.13.1 -- c:\sandbox\learn\python\django\django-api-practice\.venv\scripts\python.exe    
cachedir: .pytest_cache
django: settings: rapidapipractice.settings (from ini)
rootdir: C:\Sandbox\Learn\Python\Django\django-api-practice, inifile: pytest.ini
plugins: cov-2.10.0, django-3.9.0
collected 6 items

tests/test_users_api.py::test_get_usrers_on_empty_db_returns_empty_list PASSED [ 16%]
tests/test_users_api.py::test_get_usrers_returns_empty_list_of_users PASSED [ 33%]
tests/test_users_api.py::test_read_existing_user_returns_user_info PASSED [ 50%]
tests/test_users_api.py::test_read_not_existing_user_returns_404 PASSED  [ 66%]
tests/test_users_api.py::test_put_user_creates_user PASSED               [ 83%]
tests/test_users_api.py::test_can_read_api_root PASSED                   [100%]

--------- coverage: platform win32, python 3.7.6-candidate-1 ---------
Name                           Stmts   Miss  Cover
--------------------------------------------------
api\__init__.py                    0      0   100%
api\admin.py                       1      0   100%
api\apps.py                        3      3     0%
api\migrations\__init__.py         0      0   100%
api\models.py                      1      0   100%
api\serializers.py                10      0   100%
api\tests.py                       1      1     0%
api\views.py                      10      0   100%
rapidapipractice\__init__.py       0      0   100%
rapidapipractice\asgi.py           4      4     0%
rapidapipractice\settings.py      19      0   100%
rapidapipractice\urls.py           9      0   100%
rapidapipractice\wsgi.py           4      4     0%
--------------------------------------------------
TOTAL                             62     12    81%


============================== 6 passed in 1.09s ============================== 
```





# Create the project (Notes)

## Setup Django project

```bash
$ mkdir rapid-api-practice
$ cd rapid-api-practice

# Create and activate virtual environment
$ py -3.7 -m venv .venv
$ source .venv/Scripts/activate
$ python -m pip install --upgrade pip

$ pip install django
$ django-admin startproject rapidapipractice .
$ django-admin startapp api
$ python manage.py makemigrations
$ python manage.py migrate
#
$ python manage.py createsuperuser
# ivang/django
# ivan.georgiev@gmail.com

```



```bash
$ pip install djangorestframework
```

## Create api application

```bash
$ cd rapidapipractice/api && touch serializers.py
```

#### api/serializers.py

```python
from django.contrib.auth.models import User, Group
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']
```



#### api/views.py

```python
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from .serializers import UserSerializer, GroupSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

```

#### urls.py

```python
from django.urls import include, path
from rest_framework import routers
from api import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)

# Setup automatic URL routing
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
```



#### settings.py

Add following items to `INSTALLED_APPS` list: `rapidapipractice.api`, `rest_framework`:

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'api',
    'rest_framework',
]
```



Add at the end of `settings.py`

```python
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10
}
```

## Run the server



```bash
$ python manage.py runserver
```



## Unit Testing

To test our project we are going to use in-memory SQLite database with a user created.

### Setting Up

We are going to use pytest with pytest-django plugin:

```bash
$ pip install pytest pytest-django pytest-cov
```

### pytest.ini

Create `pytest.ini`  in the root of the application

```ini
[pytest]
DJANGO_SETTINGS_MODULE = rapidapipractice.settings
```

### Fixtures

Number of useful fixtures are provided by `pytest-django`.

#### In-Memory SQLite

We define all fixtures in `conftest.py`.  In this module we also update Django settings to use in-memory SQLite database:

```python
from rapidapipractice import settings

settings.DATABASES['default'] = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
```



#### Initialize test database (`test_db` fixture)

We will create a `test_db` fixture which initializes the database and creates a user (`username=ivang;email=ivang@mail.com). We are going to use this user later in tests.

Add following to `conftest.py`

```python
import pytest
from django.core import management

@pytest.fixture
def test_db():
    """
    Initialize the test database. Note that this fixture should be
    used with test-cases marked with @pytest.mark.django_db
    """
    fixture_data = {
        'users': [
            { 'username': 'ivang', 'email': 'ivan.georgiev@mail.com'}
        ]
    }
    management.call_command('makemigrations', verbosity=0, interactive=False)
    management.call_command('migrate', verbosity=0, interactive=False)
    for user_info in fixture_data['users']:
        management.call_command('createsuperuser', verbosity=0, interactive=False,
                **user_info)
    yield fixture_data
```

The fixture returns fixture data so that it could be used in test cases.

#### Final `conftest.py`

```python 
import pytest
from django.core import management
from rapidapipractice import settings

settings.DATABASES['default'] = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }


@pytest.fixture
def test_db():
    """
    Initialize the test database. Note that this fixture should be
    used with test-cases marked with @pytest.mark.django_db
    """
    fixture_data = {
        'users': [
            { 'username': 'ivang', 'email': 'ivan.georgiev@mail.com'}
        ]
    }
    management.call_command('makemigrations', verbosity=0, interactive=False)
    management.call_command('migrate', verbosity=0, interactive=False)
    for user_info in fixture_data['users']:
        management.call_command('createsuperuser', verbosity=0, interactive=False,
                **user_info)
    yield fixture_data
```

### Executing tests

```bash
$ pytest -vv --cov=rapidapipractice --cov=api --cov-report=term
```



### Test Cases for Users API

We will place our Users API test cases in `tests/test_users_api.py`

#### First Test Case - Smoke Test

We will start with reading the API root url and confirming it returns OK http response.

Add following to `tests/test_users_api.py`

```python
def test_can_read_api_root(client):
    response = client.get('/api/')
    assert response.status_code == 200
```

The `client` fixture is provided by `pytest-django` plugin.

#### Test Case: Read existing user

```python
import pytest

@pytest.mark.django_db
def test_read_existing_user_returns_user_info(client, test_db):
    response = client.get('/api/users/1/')
    assert response.status_code == 200
    assert response.data['username'] == 'ivang'
    assert response.data['email'] == 'ivan.georgiev@mail.com'
```

`import pytest` is necessary for the `django_db` mark. The `django_db` mark is provided by the `pytest-django` plugin. It causes the Django database to be initialized before calling the test case.

#### Test Case: Read non-existent user

Add following to `tests/test_users_api.py`

```python
@pytest.mark.django_db
def test_read_not_existing_user_returns_404(client, test_db):
    response = client.get('/api/users/101/')
    assert response.status_code == 404
```

#### Test Case: Get users returns empty list on empty database

```python
@pytest.mark.django_db
def test_get_usrers_on_empty_db_returns_empty_list(client):
    response = client.get('/api/users/')
    assert response.status_code == 200
    assert isinstance(response.data['results'], list)
    assert [] == response.data['results']
```



#### Test Case: Get users returns a list of users

```python
@pytest.mark.django_db
def test_get_usrers_returns_empty_list_of_users(client, test_db):
    response = client.get('/api/users/')
    assert response.status_code == 200
    assert isinstance(response.data['results'], list)
    assert 1 == len(response.data['results'])
    actual = response.data['results'][0]
    assert 'ivang' == actual['username']
```



#### Test Case: Put user creates a user

```python
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
```



# References

## Django General

* [Top 10 Django Mistakes](https://www.toptal.com/django/django-top-10-mistakes)
* [Advanced Tutorial: How to write reusable apps](https://docs.djangoproject.com/en/3.0/intro/reusable-apps/) (Django)
* [How to Build an API in Python (with Django)](https://rapidapi.com/blog/python-django-rest-api-tutorial/)

## Unit Testing

* [pytest-django](https://pytest-django.readthedocs.io/en/latest/)
* [Testing in Django](https://docs.djangoproject.com/en/3.0/topics/testing/) (Django)
* [Testing Your Django App With Pytest](https://djangostars.com/blog/django-pytest-testing/)