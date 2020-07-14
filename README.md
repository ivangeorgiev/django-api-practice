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
collected 3 items


tests/test_smoke.py::test_get_user PASSED                                [ 33%]
tests/test_smoke.py::test_create_user PASSED                             [ 66%]
tests/test_smoke.py::test_can_read_api_root PASSED                       [100%] 

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


============================== 3 passed in 1.23s ============================== 
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



## Testing

```bash
$ pip install pytest pytest-django pytest-cov
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