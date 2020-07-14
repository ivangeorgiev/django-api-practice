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
    # management.call_command('makemigrations', verbosity=0, interactive=False)
    # management.call_command('migrate', verbosity=0, interactive=False)
    for user_info in fixture_data['users']:
        management.call_command('createsuperuser', verbosity=0, interactive=False,
                **user_info)
    yield fixture_data

