import pytest
from django.core import management
from rapidapipractice import settings

settings.DATABASES['default'] = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }


@pytest.fixture
def test_db():
    management.call_command('makemigrations', verbosity=0, interactive=False)
    management.call_command('migrate', verbosity=0, interactive=False)
    management.call_command('createsuperuser', username='ivang', email='ivan.georgiev@mail.com', verbosity=0, interactive=False)
    yield None

