import requests
import sqlite3
import logging
import os
from dotenv import load_dotenv

load_dotenv()

conn = sqlite3.connect('whatever.sqlite')
cursor = conn.cursor()

# def dbtest():
#     cursor.execute('SELECT * FROM roster')
#     rows = cursor.fetchall()
#     for row in rows:
#         print(row)

def db_update_roster():
    roster = get_roster()
    for name in roster:
        cursor.execute("SELECT id FROM roster WHERE name = ?", (name,))
        result = cursor.fetchone()

        # print(result)
        if result is None:
            cursor.execute('INSERT INTO roster (name) VALUES (?)', (name, ))
            logging.info('%s added to roster', name)
            # print(f'{name} wurde hinzugefügt')
        else:
            # print(f'{name} ist bereits vorhanden')
            logging.info('%s already in roster', name)
    conn.commit()
    conn.close()

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