# django-api-practice

REST API with Django and Django REST Framework

Based on: https://rapidapi.com/blog/python-django-rest-api-tutorial/

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