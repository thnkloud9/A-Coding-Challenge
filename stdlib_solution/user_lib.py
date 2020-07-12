import secrets
import hashlib
import os
import binascii
from datetime import datetime
from sqlite3 import Error
from db_utils import create_connection, create_table


def hash_password(password):
    """Hash a password for storing.
    :param password: string
    :return: hashed password
    """
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac(
        'sha512', password.encode('utf-8'), salt, 100000)
    pwdhash = binascii.hexlify(pwdhash)
    return (salt + pwdhash).decode('ascii')


def verify_password(stored_password, provided_password):
    """Verify a stored password against one provided by user
    :param stored_password:
    :param provided_password:
    :return: boolean
    """
    salt = stored_password[:64]
    stored_password = stored_password[64:]
    pwdhash = hashlib.pbkdf2_hmac('sha512',
                                  provided_password.encode('utf-8'),
                                  salt.encode('ascii'),
                                  100000)
    pwdhash = binascii.hexlify(pwdhash).decode('ascii')
    return pwdhash == stored_password


def user_signup(conn, user):
    """Create a new user into the users table
    :param conn:
    :param user: dict
    :return: user id
    """
    token = secrets.token_urlsafe(16)
    sql = ''' INSERT INTO users(name,email,password,is_active,login_attempts,last_login_attempt,token)
        VALUES(?,?,?,?,?,?,?) '''
    try:
        cur = conn.cursor()
        cur.execute(sql, (
            user['name'],
            user['email'],
            hash_password(user['password']),
            0,
            0,
            None,
            token
        ))
        cur.close()

        return cur.lastrowid
    except Error as e:
        print(e)


def user_activate(conn, user_id, token):
    """Create a new task
    :param conn:
    :param user_id:
    :param token:
    :return: user id
    """

    sql = '''
        UPDATE users SET is_active = 1
        WHERE token = ? AND id = ?
        '''
    try:
        cur = conn.cursor()
        cur.execute(sql, (token, user_id))
        result = cur.lastrowid
        cur.close()
    except Error as e:
        print(e)

    return result


def user_find_by_email(conn, email):
    """Get user data by email
    :param: conn: Connection object
    :param: email: string
    :return: results
    """
    currtime = datetime.now()
    find_user_sql = '''SELECT * FROM users
        WHERE email = ?
        '''
    try:
        cur = conn.cursor()
        cur.execute(find_user_sql, [email])
        results = cur.fetchone()

    except Error as e:
        print(e)

    return results


def user_login(conn, email, password):
    """Login a user with email and password
    :param: conn: Connection object
    :param: email: string
    :param: password: string
    :return: user:
    """
    currtime = datetime.now()
    user = user_find_by_email(conn, email)

    if not user:
        return None

    try:
        cur = conn.cursor()
        if not verify_password(user[3], password):
            # password does not match!
            # incr login_attempts and update last_login_attempt for email
            update_user_sql = '''
                UPDATE users
                SET login_attempts = login_attempts + 1,
                last_login_attempt = ?
                WHERE email = ?
                '''

            cur.execute(update_user_sql, [
                currtime,
                email
            ])
            cur.close()

            return None
        else:
            # Return None if user is not activated
            if (user[4] != 1):
                return None

            # Calculate time since last login
            minutes = 0
            if user[6]:
                difference = datetime.now() - user[6]
                minutes = (difference.seconds // 60) % 60
            # Return None if failed attempts > 3 and last_login_attempt < 1
            # hour ago
            print(user[5], minutes)
            if ((user[5] >= 3) and (minutes < 60)):
                return None

            # reset login attempts and last_login_attempt
            print('reset login_attempts')
            update_user_sql = '''
                UPDATE users
                SET login_attempts = 0,
                last_login_attempt = ?
                WHERE email = ?
                '''

            cur.execute(update_user_sql, [
                currtime,
                email
            ])
            cur.close()

            user = user_find_by_email(conn, email)

    except Error as e:
        print(e)

    return user
