import pytest
from django.core import management


@pytest.fixture
def empty_db(settings, db):
    """
    Initialize empty database.
    """
    settings.DATABASES['default'] = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
    yield db


@pytest.fixture
def test_db(empty_db):
    """
    Initialize the fixture/test database with records.
    """
    fixture_data = {
        'users': [
            { 'username': 'ivang', 'email': 'ivan.georgiev@mail.com'}
        ]
    }
    # management.call_command('makemigrations', verbosity=0, interactive=False)
    # management.call_command('migrate', verbosity=0, interactive=False)
    for user_info in fixture_data['users']:
        management.call_command('createsuperuser', verbosity=0, interactive=False,
                **user_info)
    yield fixture_data

