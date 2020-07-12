import os
from db_utils import create_connection
from setup import main
from user_lib import (
    user_signup,
    user_login,
    user_activate,
    user_find_by_email
)

test_db = 'test_sqlite.db'
conn = create_connection(test_db)


def test_setup():
    main(test_db)
    assert os.path.isfile(test_db) == True


def test_user_signup():
    user_data = {
        'name': 'tester',
        'email': 'tester@tester.com',
        'password': 'password'
    }
    user_id = user_signup(conn, user_data)
    assert user_id is not None


def test_login_fails_without_activation():
    user = user_login(conn, 'tester@tester.com', 'password')
    assert user is None


def test_user_activate():
    user_data = user_find_by_email(conn, 'tester@tester.com')
    user = user_activate(conn, user_data[0], user_data[7])
    assert user is not None


def test_user_login():
    user = user_login(conn, 'tester@tester.com', 'password')
    assert user is not None


def test_user_login_failed_attempt_lockout():
    for x in range(3):
        user = user_login(conn, 'tester@tester.com', 'badpassword')
        assert user is None

    user = user_login(conn, 'tester@tester.com', 'password')
    assert user is None


def test_teardown():
    os.remove(test_db)
    assert os.path.isfile(test_db) == False
