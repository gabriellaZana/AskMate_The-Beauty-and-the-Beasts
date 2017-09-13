import time
from config import Config
import psycopg2
import psycopg2.extras
from datetime import datetime


def open_database():
    try:
        connection_string = Config.DB_CONNECTION_STR
        connection = psycopg2.connect(connection_string)
        connection.autocommit = True
    except psycopg2.DatabaseError as exception:
        print(exception)
    return connection


def connection_handler(function):
    def wrapper(*args, **kwargs):
        connection = open_database()
        dict_cur = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        ret_value = function(dict_cur, *args, **kwargs)
        dict_cur.close()
        connection.close()
        return ret_value
    return wrapper


@connection_handler
def query_handler(cursor, querystring, *args, **kwargs):
    cursor.execute(querystring, *args, **kwargs)
    try:
        result = cursor.fetchall()
        return result
    except:
        pass


def reputation_counter(amount, table, table_id):
    user_id = query_handler("SELECT users_id FROM " + table + " WHERE id = %s", (table_id,))
    query_handler("UPDATE users SET reputation = reputation + " + amount + " WHERE id = %s", (user_id[0]['users_id'],))