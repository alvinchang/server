import os
import sqlite3

USERS_DB = "users.sqlite3"

USERS_DB_PATH = os.path.dirname(__file__) + "/" + USERS_DB

"""
USERS:
user_id | user_name | first_name | last_name | email
----------------------------------------------------
"""


def init_db_connection():
    """
    Initializes a db connection to the database specified.

    :return:
    """
    try:
        conn = sqlite3.connect(USERS_DB_PATH)
        return conn
    except Exception as e:
        raise DatabaseConnectionError(e.message)


class DatabaseConnectionError(ValueError):

    def __init__(self, msg):
        super(DatabaseConnectionError, self).__init__(msg)


def insert_user_in_db(users):
    """
    Inserts a user into this row.

    :param users: the user in which to insert.
    :type users: List[User]
    :return:
    """
    conn = init_db_connection()
    user_values = [(user.user_name, user.first_name, user.last_name, user.email) for user in users]
    try:
        with conn:
            cursor = conn.cursor()
            insert_sql = """
                INSERT INTO USERS(user_name, first_name, last_name, email) VALUES(?,?,?,?);
            """
            cursor.executemany(insert_sql,
                               user_values)
            conn.commit()
    except sqlite3.IntegrityError as e:
        raise DatabaseError("Data Integrity Error: {}".format(e.message))
    except Exception as e:
        raise DatabaseError("Database Error: {}".format(e.message))


class DatabaseError(ValueError):
    def __init__(self, msg):
        super(DatabaseError, self).__init__(msg)


def get_all_user_names():
    conn = init_db_connection()
    with conn:
        cursor = conn.cursor()
        select_sql = """
                SELECT user_name FROM USERS;
            """
        cursor.execute(select_sql)
        return cursor.fetchall()


def initialize_db(reset=False):
    """
    Initializes the USERS database

    :param reset: whether or not to delete the previous table if exists.
    :type reset: bool

    :return:
    """
    conn = init_db_connection()
    with conn:
        cursor = conn.cursor()
        if reset:
            cursor.execute("""
                DROP TABLE IF EXISTS USERS;
            """)
        cursor.execute("""
            CREATE TABLE USERS (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_name TEXT UNIQUE,
                first_name TEXT,
                last_name TEXT,
                email TEXT
            );
        """)

        cursor.execute("""
            INSERT INTO USERS(user_name, first_name, last_name, email) VALUES('JohnDoe','John','Doe',
            'John.Doe@email.com');
        
        """)
        conn.commit()


if __name__ == "__main__":
    initialize_db(reset=True)


