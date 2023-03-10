import requests
import sqlite3
import logging
import os
from datetime import date, datetime
from dotenv import load_dotenv
from helper import open_db, close_db

load_dotenv()



# def dbtest():
#     cursor.execute('SELECT * FROM roster')
#     rows = cursor.fetchall()
#     for row in rows:
#         print(row)

def db_update_roster():
    conn, cursor = open_db()

    today = datetime.today()
    today_formatted = today.strftime("%d.%m.%Y, %H:%M")

    roster = get_roster()
    for name in roster:
       
        cursor.execute("SELECT id FROM roster WHERE name = ?", (name,))
        result = cursor.fetchone()


        # print(result)
        if result is None:
            cursor.execute('INSERT INTO roster (name, updatedAt) VALUES (?, ?)', (name, today_formatted))
            logging.info('%s added to roster', name)
            # print(f'{name} wurde hinzugefügt')
        else:
            cursor.execute('UPDATE roster SET name = ?, updatedAt = ? WHERE id = ?', (name, today_formatted, result[0]))
            logging.info('%s already in roster', name)
    
    close_db(conn, cursor)

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
        roster.append(player['name'])


    return roster

# get_roster()
# dbtest()
# db_update_roster()