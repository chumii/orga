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

# def db_query_wait(query, params=None, fetch=None, type=None, wait=0.1):
#     while True:
#         try:
#             conn = sqlite3.connect('whatever.sqlite')
#             cursor = conn.cursor()
#             if params is None:
#                 cursor.execute(query)
#                 logging.info("Query done: params = %s", params)
#             else:
#                 cursor.execute(query, params)
#                 logging.info("Query done: query = %s, params = %s", query, params)
#             if fetch == "fetchone":
#                 result = cursor.fetchone()
#                 logging.info("Query done - fetchone: %s", result)
#             elif fetch == "fetchall":
#                 result = cursor.fetchall()
#                 logging.info("Query done - fetchall: %s", result)
#             elif fetch == "fetchmany":
#                 result = cursor.fetchmany()
#                 logging.info("Query done - fetchmany: %s", result)
#             elif fetch == None:
#                 logging.info("Query done - fetch = None")
#                 cursor.close()
#                 conn.commit()
#                 conn.close()
#                 return
#             else:
#                 raise ValueError("Invalid fetch parameter: {}".format(fetch))                
#             cursor.close()
#             conn.commit()
#             conn.close()
#             return result
#         except sqlite3.OperationalError as e:
#             # if "database is locked" not in str(e):
#             #     logging.info(str(e))
#             #     raise
#             # if params is None:
#             #     logging.error("DB locked: %s - query = %s", str(e), query)
#             # else:
#             #     logging.error("DB locked: %s - query = %s, params = %s", str(e), query, params)
#             # time.sleep(wait)
#             if "database is locked" in str(e):
#                 if params is None:
#                     logging.warning("DB locked: %s - query = %s", str(e), query)
#                 else:
#                     logging.warning("DB locked: %s - query = %s, params = %s", str(e), query, params)
#             else:
#                 logging.error(str(e))
#                 raise
#             time.sleep(wait)

from PySide6.QtSql import QSqlDatabase, QSqlQuery, QSqlQueryModel

def db_query_wait(db, query, params=None, fetch=None, type=None, wait=0.1, print=True, func=None):
    result = None
    while True:
        # db = QSqlDatabase.addDatabase('QSQLITE')
        # db.setDatabaseName('whatever.sqlite')
        if not db.open():
            logging.error("Failed to open database")
            return

        query_obj = QSqlQuery(db)
        if params is None:
            query_obj.prepare(query)
            query_str = query
        else:
            query_obj.prepare(query)
            for i, param in enumerate(params):
                query_obj.bindValue(i, param)
            query_str = query + " with parameters: " + str(params)
        
        if not query_obj.exec():
            logging.error("Failed to execute query: %s", query_str)
            logging.error(query_obj.lastError().text())
            return
        
        if fetch == "fetchone":
            # if query_obj.next():
            #     result = query_obj.value(0)
            if query_obj.next():
                record = query_obj.record()
                result = []
                for i in range(record.count()):
                    result.append(query_obj.value(i))
            else:
                result = None
            if print:
                logging.info("Query done - func: %s - fetchone: %s",func , result)
            else:
                logging.info("Query done - func: %s - fetchone",func)
        elif fetch == "fetchall":
            result = []
            while query_obj.next():
                row = []
                for i in range(query_obj.record().count()):
                    row.append(query_obj.value(i))
                result.append(row)
            if print:
                logging.info("Query done - func: %s - fetchall: %s",func , result)
            else:
                logging.info("Query done - func: %s - fetchall",func)
        elif fetch == "fetchmany":
            result = []
            for i in range(type):
                if query_obj.next():
                    row = []
                    for j in range(query_obj.record().count()):
                        row.append(query_obj.value(j))
                    result.append(row)
            if print:
                logging.info("Query done - func: %s -  fetchmany: %s",func, result)
            else:
                logging.info("Query done - func: %s - fetchmany",func)
        elif fetch is None:
            logging.info("Query done - func: %s - fetch: None", func)
        else:
            raise ValueError("Invalid fetch parameter: {}".format(fetch))
        
        # db.close()
        db.commit()
        return result

