import sqlite3
import logging
import time

def open_cursor(conn):
    # conn = sqlite3.connect('whatever.sqlite')
    cursor = conn.cursor()
    # return conn, cursor
    return cursor

def close_cursor(conn, cursor):
    conn.commit()
    cursor.close()
    # conn.close()

# result = db_query_wait(conn, "SELECT * FROM users WHERE age > ? AND name = ?", (25, "John"), fetch="fetchall")
# def db_query_wait(conn, query, params=None, fetch=None, type=None, wait=0.1):
def db_query_wait(query, params=None, fetch=None, type=None, wait=0.1):
    while True:
        try:
            conn = sqlite3.connect('whatever.sqlite')
            cursor = conn.cursor()
            if params is None:
                cursor.execute(query)
                logging.info("Query done: params = %s", params)
            else:
                cursor.execute(query, params)
                logging.info("Query done: query = %s, params = %s", query, params)
            if fetch == "fetchone":
                result = cursor.fetchone()
                logging.info("Query done - fetchone: %s", result)
            elif fetch == "fetchall":
                result = cursor.fetchall()
                logging.info("Query done - fetchall: %s", result)
            elif fetch == "fetchmany":
                result = cursor.fetchmany()
                logging.info("Query done - fetchmany: %s", result)
            elif fetch == None:
                logging.info("Query done - fetch = None")
                cursor.close()
                conn.commit()
                conn.close()
                return
            else:
                raise ValueError("Invalid fetch parameter: {}".format(fetch))                
            cursor.close()
            conn.commit()
            conn.close()
            return result
        except sqlite3.OperationalError as e:
            if "database is locked" not in str(e):
                logging.info(str(e))
                raise
            logging.error("DB locked: %s", str(e))
            time.sleep(wait)

# from helper import open_db, close_db
# cursor = open_cursor)
# close_cursor(conn, cursor)

