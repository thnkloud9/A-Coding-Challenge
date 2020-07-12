import settings
from db_utils import create_connection, create_table
from sqlite3 import Error


def main(settings=settings):
    """
    Creates sqlite database and users table
    """
    database = settings.DATABASE
    sql_create_users_table = """CREATE TABLE IF NOT EXISTS users (
       id integer PRIMARY KEY,
       name text NOT NULL,
       email text NOT NULL UNIQUE,
       password text NOT NULL,
       is_active integer NOT NULL,
       login_attempts integer NOT NULL,
       last_login_attempt timestamp,
       token text NOT NULL
    );"""

    # create a database connection
    conn = create_connection(database)

    if conn is not None:
        try:
            # create users table
            create_table(conn, sql_create_users_table)
        except Error as e:
            print(e)
        finally:
            conn.close()

    else:
        print('Error! could not create database connection')
        exit(0)


if __name__ == '__main__':
    main()
