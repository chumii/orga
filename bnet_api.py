import json
import requests
import urllib.parse
import sqlite3
import os
from dotenv import load_dotenv

load_dotenv()

conn = sqlite3.connect('whatever.sqlite')
cursor = conn.cursor()

def bnet_auth():
    client_id = os.getenv('BNET_CLIENT_ID')
    client_secret =  os.getenv('BNET_CLIENT_SECRET')

    oauth_url = "https://oauth.battle.net/authorize"
    token_url = "https://oauth.battle.net/token"

    data = {
        'grant_type': 'client_credentials',
    }

    token = requests.post('https://oauth.battle.net/token', data=data, auth=(client_id, client_secret)).json()
    access_token = token['access_token']

    return access_token



# test = 109873 # sharpeye-bracers

#item 
def get_item_slot(itemId, locale = "en_US"):
    token = bnet_auth()  
    item_endpoint = f'https://us.api.blizzard.com/data/wow/item/{itemId}?namespace=static-us&locale={locale}&access_token={token}'
    
    response = requests.get(item_endpoint)
    response_obj = json.loads(response.content)

    item_slot = response_obj['inventory_type']['type']
    
    return item_slot

def get_item_name_by_id(item_id, locale = "en_US"):
    token = bnet_auth()    
    item_endpoint = f'https://eu.api.blizzard.com/data/wow/item/{item_id}?namespace=static-eu&locale={locale}&access_token={token}'

    response = requests.get(item_endpoint)
    response_obj = json.loads(response.content)
    name = response_obj['name']
    return name

def add_single_item_by_id(item_id, cursor, locale = "en_US"):
    token = bnet_auth()    
    item_endpoint = f'https://eu.api.blizzard.com/data/wow/item/{item_id}?namespace=static-eu&locale={locale}&access_token={token}'

    response = requests.get(item_endpoint)
    response_obj = json.loads(response.content)

    item_id = item_id
    item_name = response_obj['name']
    item_source_dungeon = "BOE"
    item_slot = response_obj['inventory_type']['type']
    item_source_encounter = "Trash"

    # conn = sqlite3.connect('whatever.sqlite')
    # cursor = conn.cursor()

    cursor.execute("SELECT item_id FROM items WHERE item_id = ?", (item_id,))
    result = cursor.fetchone()

    # print(result)
    if result is None:
        cursor.execute('INSERT INTO items (item_id, item_name, item_source_dungeon, item_source_encounter, item_slot) VALUES (?, ?, ?, ?, ?)', (item_id, item_name, item_source_dungeon, item_source_encounter, item_slot, ))
        # print(f"{item_id} wurde hinzugefügt")
    # else:
    #     print(f"{item_id} ist bereits vorhanden")

    # conn.commit()
    # conn.close()

    return
    # print(f"item_id: {item_id}")
    # print(f"item_name: {item_name}")
    # print(f"item_slot: {item_slot}")
    # print(f"item_source_dungeon: {item_source_dungeon}")
    # print(f"item_source_encounter: {item_source_encounter}")
    #201992

# add_single_item_by_id("201992")

# eranog 2480

# expansion -> instance -> encounter

# journal expansion (list of instances per expansion)
def get_journal_expansion(journalExpansionId, locale = "en_US"):
    token = bnet_auth()    
    journal_endpoint = f'https://us.api.blizzard.com/data/wow/journal-expansion/{journalExpansionId}?namespace=static-us&locale={locale}&access_token={token}'
    
    response = requests.get(journal_endpoint)
    response_obj = json.loads(response.content)

    instance_list = []

    # return response_obj['dungeons']
    for instance in response_obj['dungeons']:
        instance_list.append(instance['id'])
    
    for instance in response_obj['raids']:
        instance_list.append(instance['id'])
    
    return instance_list
    # print(response_obj['dungeons'])
    # print(response_obj['items'][0])

# get_journal_expansion("503")

# journal instance (list of encounter per instance) 
def get_journal_instance(journalInstanceId, locale = 'en_US'):
    token = bnet_auth()    
    journal_endpoint = f'https://us.api.blizzard.com/data/wow/journal-instance/{journalInstanceId}?namespace=static-us&locale={locale}&access_token={token}'
    
    response = requests.get(journal_endpoint)
    response_obj = json.loads(response.content)

    encounter_list = []
    instance_name = response_obj['name']
    
    for encounter in response_obj['encounters']:
        encounter_list.append(encounter['id'])
    
    # print(instance_name)
    # print(encounter_list)

    return instance_name, encounter_list
    # return response_obj['encounters']
    # print(response_obj['name'])
    # print(response_obj['encounters'][0]['id'])

# get_journal_instance("1201")


#journal encounter (list of items per encounter)
def get_journal_encounter(journalEncounterId, instance, locale = "en_US"):
    item_source_dungeon = instance
    token = bnet_auth()    
    journal_endpoint = f'https://us.api.blizzard.com/data/wow/journal-encounter/{journalEncounterId}?namespace=static-us&locale={locale}&access_token={token}'

    response = requests.get(journal_endpoint)
    response_obj = json.loads(response.content)

    item_source_encounter = response_obj['name']
    item_list = response_obj['items']
    # print(response_obj)

    # print("Instance Name: " + item_source_dungeon)
    # print("Encounter Name: " + item_source_encounter)

    
    item_db = []

    for item in item_list:
        item_name = item['item']['name']
        item_id = item['item']['id']
        item_slot = get_item_slot(item_id)
        if item_slot == "HOLDABLE":
            item_slot = "OFFHAND"
        item_dict = {}
        item_dict['item_id'] = item_id
        item_dict['item_name'] = item_name
        item_dict['item_slot'] = item_slot
        item_dict['item_source_dungeon'] = item_source_dungeon
        item_dict['item_source_encounter'] = item_source_encounter

        item_db.append(item_dict)

        # print("Item Name: " + item_name)
        # print("Item ID: " + str(item_id))
        # print("Item Slot: " + item_slot)
        # item_id = item

    # print(response_obj['name'])
    # print(response_obj['items'][0])
    return item_db
    

# get_journal_encounter("2509", "Bla")



def get_all_items(journalExpansionId):
    instances = get_journal_expansion(journalExpansionId)

    all_items = []

    for instance in instances:
        instance_name, encounter_list = get_journal_instance(instance)
        # print(name)
        # print(encounter_list)
        for encounter in encounter_list:
            all_items.append(get_journal_encounter(encounter, instance_name))
            # print(instance_name)
            # print(encounter)
            

        print("Finished get items for: " + instance_name)    
        # print(all_items)
        # for sublist in all_items:
        #     for item in sublist:
        #         print(item['item_source_encounter'] + " - " + item['item_name'])
    
    return all_items

    # print(instances)

# get_all_items("503")

# dragonflight journal id 503
# m+ dungeons journal id 505

def db_update_items():
    journal_ids = ["503", "505"]

    all_items = []

    for journalId in journal_ids:
        all_items = get_all_items(journalId)


    for sublist in all_items:    
        for item in sublist:
            cursor.execute("SELECT item_id FROM items WHERE item_id = ?", (item['item_id'],))
            result = cursor.fetchone()

            # print(result)
            if result is None:
                cursor.execute('INSERT INTO items (item_id, item_name, item_source_dungeon, item_source_encounter, item_slot) VALUES (?, ?, ?, ?, ?)', (item['item_id'], item['item_name'], item['item_source_dungeon'], item['item_source_encounter'], item['item_slot'], ))
                print(f"{item['item_id']} wurde hinzugefügt")
            else:
                print(f"{item['item_id']} ist bereits vorhanden")

    conn.commit()
    conn.close()

# db_update_items()