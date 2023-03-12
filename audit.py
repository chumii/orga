import requests
import sqlite3
import logging
import os
from datetime import date, datetime
from dotenv import load_dotenv
from helper import open_cursor, close_cursor, db_query_wait

load_dotenv()



# def dbtest():
#     cursor.execute('SELECT * FROM roster')
#     rows = cursor.fetchall()
#     for row in rows:
#         print(row)

def db_update_roster(db):   

    today = datetime.today()
    today_formatted = today.strftime("%d.%m.%Y, %H:%M")

    roster = get_roster()
    # print(roster)
    for name in roster:
        # cursor = open_cursor(conn)
        # cursor.execute("SELECT id FROM roster WHERE name = ?", (name,))
        # result = cursor.fetchone()
        # close_cursor(conn, cursor)
        query = "SELECT id FROM roster WHERE name = ?"
        params = (name,)
        result = db_query_wait(db, query, params=params, fetch="fetchone", func="db_update_roster get player from roster")

        # print(result)
        if result is None:
            # cursor = open_cursor(conn)
            # cursor.execute('INSERT INTO roster (name, updatedAt) VALUES (?, ?)', (name, today_formatted))
            # close_cursor(conn, cursor)
            query = "INSERT INTO roster (name, updatedAt) VALUES (?, ?)"
            params = (name, today_formatted)
            db_query_wait(db, query, params=params, func="db_update_roster insert new player")
            logging.info('%s added to roster', name)
            # print(f'{name} wurde hinzugefügt')
        else:
            # cursor = open_cursor(conn)
            # cursor.execute('UPDATE roster SET name = ?, updatedAt = ? WHERE id = ?', (name, today_formatted, result[0]))
            # close_cursor(conn, cursor)
            query = "UPDATE roster SET name = ?, updatedAt = ? WHERE id = ?"
            params = (name, today_formatted, result[0])
            db_query_wait(db, query, params=params, func="db_update_roster update player")
            logging.info('%s already in roster', name)
    
    

def get_roster():

    roster = []

    api_key = os.getenv('AUDIT_API_KEY')
    url_roster = "https://wowaudit.com/v1/characters"
    headers = {
                'Accept': 'application/json',
                'Authorization': api_key
            }

    data_roster = requests.get(url_roster, headers=headers).json()

    for player in data_roster:
        # print(player)
        roster.append(player['name'])


    return roster

# get_roster()
# dbtest()
# db_update_roster()