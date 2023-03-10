import sqlite3

def open_db():
    conn = sqlite3.connect('whatever.sqlite')
    cursor = conn.cursor()
    return conn, cursor

def close_db(conn, cursor):
    cursor.close()
    conn.commit()
    conn.close()

# from helper import open_db, close_db
# conn, cursor = open_db()
# close_db(conn, cursor)

