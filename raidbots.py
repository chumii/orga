import requests
import json
import sqlite3
from bnet_api import add_single_item_by_id
from datetime import date, datetime
# from audit import get_roster

# raid_url = 'https://www.raidbots.com/reports/ew56A5zYveBB31LaEVdHQg'
# mplus_url = 'https://www.raidbots.com/reports/7621EqDL8NJPa29SXF1L3V'

#get current dps from sim report
def get_current_dps(report_url):
       
    response = requests.get(report_url+"/data.json")
    raid_data = json.loads(response.text)

    current_dps = raid_data['sim']['players'][0]['collected_data']['dps']['mean']
    
    return current_dps

#get player spec
def get_player_spec(report_url):
       
    response = requests.get(report_url+"/data.json")
    raid_data = json.loads(response.text)

    player_spec = raid_data['sim']['players'][0]['specialization']
    
    return player_spec

#get item id by name from database
def get_item_id(name_string):
    conn = sqlite3.connect("whatever.sqlite")
    c = conn.cursor()
    c.execute("SELECT * FROM items WHERE item_name = ?", (name_string, ))
    item = c.fetchone()
    conn.commit()
    conn.close()
    item_id = item[0]
    return item_id

# get_item_id("Mark of Ice")

def get_sim_results(report_url):
    today = datetime.today()
    today_formatted = today.strftime("%d.%m.%Y, %H:%M")
    # print(type(today))

    response = requests.get(report_url+"/data.json")
    sim_data = json.loads(response.text)
    
    
    items = sim_data['sim']['profilesets']['results']
    character_name = sim_data['sim']['players'][0]['name'].capitalize()

    conn = sqlite3.connect('whatever.sqlite')
    cu = conn.cursor()    

    character_id = cu.execute(f"SELECT * FROM roster WHERE name='{character_name}'").fetchone()[0]
    character_current_dps = cu.execute(f"SELECT * FROM roster WHERE name='{character_name}'").fetchone()[5]

    conn.commit()
    conn.close()
        
    item_list = []

    for item in items:
        url_parts = item['name'].split("/")
        item_id = url_parts[3]
        
        conn = sqlite3.connect('whatever.sqlite')
        cu = conn.cursor()
        
        
        cu.execute("SELECT * FROM items WHERE item_id = ?", (item_id, ))
        db_item = cu.fetchone()
        
        if db_item == None:
            add_single_item_by_id(item_id, cu)
            cu.execute("SELECT * FROM items WHERE item_id = ?", (item_id, ))
            db_item = cu.fetchone()
        else:
            pass
            
        sim_dps = float(item['mean'])
        
        item_list.append({'item_id': item_id,'character': character_name,'sim_dps': sim_dps})

        #calculate upgrade %
        upgrade_perc = ( ( float(sim_dps) / float(character_current_dps) ) * 100 ) - 100
        upgrade_perc = "{:.2f}".format(upgrade_perc)
        
        
        #db_data = c.execute(f"SELECT * FROM sim_results WHERE item_id='{item_id}' AND  character={character_id}").fetchone()
        

        # if db_data and db_data[3] <= sim_dps:
        #     c.execute(f"UPDATE sim_results SET sim_dps='{sim_dps}', upgrade_perc='{upgrade_perc}', updatedAt='{today_formatted}' WHERE item_id='{item_id}' AND character={character_id}")
        #     # print("updated")
        # elif not db_data:
        cu.execute('INSERT INTO sim_results (item_id, character, character_name, sim_dps, upgrade_perc, updatedAt) VALUES (?, ?, ?, ?, ?, ?)', (item_id, character_id, character_name, sim_dps, upgrade_perc, today_formatted))
        conn.commit()
        conn.close()

    #cu.close()
    # conn.commit()
        # conn.close()
    # return
    
    # return item_list
    # print(item_list)

# get_item_dps("https://www.raidbots.com/simbot/report/5FeFkwSyfAjJySBqMHF44h")

# Raid https://www.raidbots.com/simbot/report/ew56A5zYveBB31LaEVdHQg - https://www.raidbots.com/reports/ew56A5zYveBB31LaEVdHQg/data.json
# MPlus https://www.raidbots.com/simbot/report/7621EqDL8NJPa29SXF1L3V - https://www.raidbots.com/reports/7621EqDL8NJPa29SXF1L3V/data.json



# raid_dps = get_current_dps(raid_url)
# mplus_dps = get_current_dps(mplus_url)

# print("Raid: " + str(int(raid_dps)))
# print("Mplus: " + str(int(mplus_dps)))

# test = get_item_dps(mplus_url)
# print(test)


# def submit_raid(raid):
#     dps = get_current_dps(raid)
#     print("Raid:", dps)

# def submit_mplus(mplus):
#     dps = get_current_dps(mplus)
#     print("MPlus:", dps)

# roster = get_roster()

# print(roster)

# for player in roster:
#     print(player)

