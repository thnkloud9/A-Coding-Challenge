import os
import settings
from db_utils import create_connection
from setup import main
from user_lib import (
    user_signup,
    user_login,
    user_activate,
    user_find_by_email
)

settings.DATABASE = 'test_sqlite.db'

def test_setup():
    main(settings)
    assert os.path.isfile(settings.DATABASE) == True

def test_user_signup():
    user_data = {
        'name': 'tester',
        'email': 'tester@tester.com',
        'password': 'password'
    }
    user = user_signup(user_data, settings)
    assert user is not None

def test_login_fails_without_activation():
    user = user_login('tester@tester.com', 'password', settings)
    assert user is None

def test_user_activate():
    user_data = user_find_by_email('tester@tester.com', settings)
    result = user_activate(user_data[0], user_data[7], settings)
    assert result is True

def test_user_login():
    user = user_login('tester@tester.com', 'password', settings)
    assert user is not None

def test_user_login_failed_attempt_lockout():
    for x in range(3):
        user = user_login('tester@tester.com', 'badpassword', settings)
        assert user is None

    user = user_login('tester@tester.com', 'password', settings)
    assert user is None

def test_teardown():
    os.remove(settings.DATABASE)
    assert os.path.isfile(settings.DATABASE) == False