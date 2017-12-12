import os
import sqlite3

from users.users import User

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


def get_user_in_db(username):
    """
    Gets a user row based on the username (which should be unique)

    :param username:
    :type username: str
    :rtype: User
    """
    conn = init_db_connection()
    with conn:
        cursor = conn.cursor()
        select_sql = """
            SELECT * FROM USERS WHERE user_name = '?';
        """
        cursor.execute(select_sql, username)
        results = cursor.fetchall()
        if not results:
            raise DatabaseError("Could not find user_name={}".format(username))

        person_row = cursor.fetchall()[0]
        return User(
            user_name=person_row[1],
            first_name=person_row[2],
            last_name=person_row[3],
            email=person_row[4],
            user_id=person_row[0]
        )


def get_user_id_in_db(username):
    """
    Gets a user id based on the username (which should be unique)

    :param username:
    :type username: str
    :rtype: str
    """
    conn = init_db_connection()
    with conn:
        cursor = conn.cursor()
        select_sql = """
            SELECT user_id FROM USERS WHERE user_name = ?;
        """
        cursor.execute(select_sql, username)
        results = cursor.fetchall()[0]
        if not results:
            raise DatabaseError("Could not find user_name={}".format(username))
        return results[0][0]


def modify_user_email_in_db(username, new_user_email):
    """
    Modifies a user in the database.

    :param username:
    :type username: str
    """
    user_id = get_user_id_in_db(username)
    conn = init_db_connection()
    with conn:
        cursor = conn.cursor()
        select_sql = """
               UPDATE USERS SET email=? where user_id=?;
           """
        cursor.execute(select_sql, (new_user_email, user_id))


def delete_user_in_db(username):
    """
    Deletes a user in the database.

    :param username:
    :type username: str
    """
    conn = init_db_connection()
    with conn:
        cursor = conn.cursor()
        delete_sql = """
            DELETE FROM USERS WHERE user_name = ?;
        """
        cursor.execute(delete_sql, username)


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


