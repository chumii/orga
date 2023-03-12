import requests
import json
from bnet_api import get_item_name_by_id

def get_current_dps(report_url):
       
    response = requests.get(report_url)
    raid_data = json.loads(response.text)

    current_dps = raid_data['sim']['players'][0]['collected_data']['dps']['mean']

    return current_dps

def get_item_id(db, name_string):
    parts = name_string.split('/')
    item_id = parts[3]
    return item_id

def get_item_dps(report_url):

    response = requests.get(report_url)
    raid_data = json.loads(response.text)

    items = raid_data['sim']['profilesets']['results']

    item_list = []

    for item in items:
        item_id = get_item_id(db, item['name'])
        item_name = get_item_name_by_id(item_id)
        item_dps = item['mean']

        item_list.append({'id': item_id,'name': item_name,'dps': item_dps})
    
    return item_list