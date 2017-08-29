import time
from config import Config
import psycopg2
import psycopg2.extras
from datetime import datetime


def print_info(variable):
    print("Original string: {var} ({type})".format(**{
        "var": variable,
        "type": type(variable)
    }))


def sortbynumber(index=0):
    table = import_story("data/question.csv")
    table_original = import_story("data/question.csv")
    for line in table:
        line[index] = int(float(line[index]))
    for line in table_original:
        line[index] = int(float(line[index]))
    table.sort(key=lambda x: x[index])
    if table == table_original:
        for line in table:
            line[index] = int(line[index])
        table.sort(key=lambda x: x[index], reverse=True)
    export_story("data/question.csv", table)


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
        # we set the cursor_factory parameter to return with a dict cursor (cursor which provide dictionaries)
        dict_cur = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        ret_value = function(dict_cur, *args, **kwargs)
        dict_cur.close()
        connection.close()
        return ret_value
    return wrapper
