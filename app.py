from PySide6.QtWidgets import QApplication, QMainWindow, QStyledItemDelegate, QLineEdit
from PySide6 import QtSql
from PySide6.QtCore import Qt, QCoreApplication, QSortFilterProxyModel, QFileSystemWatcher
from qt.frm_main import Ui_frm_main
from audit import db_update_roster
from raidbots import get_current_dps, get_player_spec, get_sim_results
from datetime import date, datetime
import logging
import sqlite3

logging.basicConfig(filename='whatever.log', level=logging.DEBUG, format='%(asctime)s [%(levelname)s] %(message)s', datefmt='%d-%b-%y %H:%M:%S')

# DB Connection
db = QtSql.QSqlDatabase.addDatabase("QSQLITE")
db.setDatabaseName("whatever.sqlite")

# QtMainWindow
class Frm_main(QMainWindow, Ui_frm_main):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        
        self.actionBeenden.triggered.connect(self.closeApplication)
        self.tabs_main.setCurrentIndex(0)

        ###### Character Tab ######

        self.mod_roster = QtSql.QSqlRelationalTableModel()
        self.mod_roster.setTable("roster")
        # mod_roster.setRelation(1, QtSql.QSqlRelation("relationTabelle", 2))
        self.mod_roster.select()

        header_label = ['id', 'Name', 'Raid Droptimizer', 'MPlus Droptimizer', 'Spec', 'Current DPS', 'Last Update']

        for i, label in enumerate(header_label):
            self.mod_roster.setHeaderData(i, Qt.Horizontal, label)
        self.tbl_charaktere.setModel(self.mod_roster)
        self.tbl_charaktere.setColumnHidden(0, True)
        self.tbl_charaktere.setColumnWidth(1, 140)
        self.tbl_charaktere.setColumnWidth(2, 282)
        self.tbl_charaktere.setColumnWidth(3, 282)
        self.tbl_charaktere.setColumnWidth(4, 186)
        self.tbl_charaktere.setColumnWidth(5, 100)
        self.tbl_charaktere.setColumnWidth(6, 100)

        self.btn_update.clicked.connect(self.update_view)
        self.btn_update_sims.clicked.connect(self.update_sims)

        ###### Item Tab ######

        self.grab_all_items()
        self.grab_all_dungeons()
        self.grab_all_encounter()

        self.btn_item_filter_dungeon_submit.clicked.connect(self.btn_item_filter_dungeon_submit_click)
        self.btn_item_filter_encounter_submit.clicked.connect(self.btn_item_filter_encounter_submit_click)

        self.list_items.itemClicked.connect(self.on_list_item_clicked)

        self.btn_item_search.clicked.connect(self.search_items)
        self.text_item_search.returnPressed.connect(self.search_items)

        #tbl_sim_results
        self.mod_sim_results = QtSql.QSqlRelationalTableModel()
        self.mod_sim_results.setTable("sim_results")
        self.mod_sim_results.select()

        sim_results_header_label = ['ID', 'character_id', 'Name', 'DPS', 'Upgrade', 'Last Update']

        for i, label in enumerate(sim_results_header_label):
            self.mod_sim_results.setHeaderData(i, Qt.Horizontal, label)
        self.tbl_sim_results.setModel(self.mod_roster)
        self.tbl_sim_results.setColumnWidth(0, 50)
        self.tbl_sim_results.setColumnHidden(1, True)
        self.tbl_sim_results.setColumnWidth(2, 150)
        self.tbl_sim_results.setColumnWidth(3, 95)
        self.tbl_sim_results.setColumnWidth(4, 95)
        self.tbl_sim_results.setColumnWidth(5, 100)
       
        self.proxy_model = QSortFilterProxyModel()
        self.proxy_model.setFilterKeyColumn(self.mod_sim_results.fieldIndex('item_id'))        
        self.proxy_model.setSourceModel(self.mod_sim_results)

        
        self.tbl_sim_results.setModel(self.proxy_model)

        ###### Log Tab ######

        with open('whatever.log', 'r') as f:
            self.text_log_viewer.setPlainText(f.read())

        self.file_watcher = QFileSystemWatcher(["whatever.log"], self)
        self.file_watcher.fileChanged.connect(self.update_log_viewer)

    #update log viewer
    def update_log_viewer(self):
        with open('whatever.log', 'r') as f:
            self.text_log_viewer.setPlainText(f.read())

    # update roster 
    def update_view(self):
        db_update_roster()
        self.mod_roster.select()

    #update roster rows
    def update_sims(self):
        conn = sqlite3.connect('whatever.sqlite')
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM roster")
        roster = cursor.fetchall()

        conn.commit()
        conn.close()
        
        today = datetime.today()
        today_formatted = today.strftime("%d.%m.%Y, %H:%M")

        for row in roster:
            raid_url = row[2]
            mplus_url = row[3]
            raid_dps = 0
            mplus_dps = 0
            roster_id = row[0]

            if raid_url:
                spec = get_player_spec(raid_url)
                raid_dps = get_current_dps(raid_url)
            elif mplus_url:
                spec = get_player_spec(mplus_url)
                mplus_dps = get_current_dps(mplus_url)
            else:
                spec = "-"

            if raid_url and not mplus_url:
                mplus_dps = raid_dps
            if mplus_url and not raid_url:
                raid_dps = mplus_dps
            
            current_mean_dps = (raid_dps + mplus_dps) / 2

            conne = sqlite3.connect('whatever.sqlite')
            cursor = conne.cursor()
        
            # cursor.execute("UPDATE roster SET spec = ?, current_dps = ?, updatedAt = ? WHERE id = ?", (spec, int(current_mean_dps), today_formatted, roster_id))
            cursor.execute(f"UPDATE roster SET spec='{spec}', current_dps='{int(current_mean_dps)}', updatedAt='{today_formatted}' WHERE id='{roster_id}'")
            conne.commit()
            conne.close()

            if raid_url and mplus_url:
                get_sim_results(raid_url)
                get_sim_results(mplus_url)

        #####################################################################
        ### data.json von raidbots nur 1x holen und results nicht von url ### 
        #####################################################################            
        self.mod_roster.select()
        self.mod_sim_results.select()

    # add items to item list
    def grab_all_items(self, filter_dungeon="", filter_encounter=""):
        conn = sqlite3.connect("whatever.sqlite")
        c = conn.cursor()
        if filter_dungeon == "" and filter_encounter == "":
            c.execute("SELECT * FROM items")
        elif filter_dungeon != "" and filter_encounter == "":
            c.execute("SELECT * FROM items WHERE item_source_dungeon = ?", (filter_dungeon, ))
        elif filter_dungeon != "" and filter_encounter != "":
            c.execute("SELECT * FROM items WHERE item_source_dungeon = ? AND item_source_encounter = ?", (filter_dungeon, filter_encounter))
        items = c.fetchall()
        conn.commit()
        conn.close()

        self.list_items.clear()

        items_sorted = sorted(items, key=lambda x: x[1])

        for item in items_sorted:
            self.list_items.addItem(str(item[1]))

    # add dungeons to dropdown
    def grab_all_dungeons(self):
        conn = sqlite3.connect("whatever.sqlite")
        c = conn.cursor()
        c.execute("SELECT DISTINCT item_source_dungeon FROM items")
        dungeons = c.fetchall()
        conn.commit()
        conn.close()
        
        dungeons_sorted = sorted(dungeons, key=lambda x: x[0])

        for dungeon in dungeons_sorted:
            self.ddown_item_filter_dungeon.addItem(str(dungeon[0]))

    # add encounter to dropdown
    def grab_all_encounter(self, filter=""):
        conn = sqlite3.connect("whatever.sqlite")
        c = conn.cursor()
        if filter == "":
            c.execute("SELECT DISTINCT item_source_encounter FROM items")
        else:
            c.execute("SELECT DISTINCT item_source_encounter FROM items WHERE item_source_dungeon = ?", (filter, ))
        encounters = c.fetchall()
        conn.commit()
        conn.close()
        
        encounters_sorted = sorted(encounters, key=lambda x: x[0])

        self.ddown_item_filter_encounter.clear()

        for encounter in encounters_sorted:
            self.ddown_item_filter_encounter.addItem(str(encounter[0]))

    # dungeon filter button clicked
    def btn_item_filter_dungeon_submit_click(self):
        selected = self.ddown_item_filter_dungeon.currentText()
        self.grab_all_encounter(selected)
        self.grab_all_items(selected)
    
    # encounter filter button clicked
    def btn_item_filter_encounter_submit_click(self):
        selected_dungeon = self.ddown_item_filter_dungeon.currentText()
        selected_encounter = self.ddown_item_filter_encounter.currentText()
        self.grab_all_items(selected_dungeon, selected_encounter)

    # click on item in list
    def on_list_item_clicked(self, item):
        item_name = item.text()

        conn = sqlite3.connect("whatever.sqlite")
        c = conn.cursor()
        c.execute("SELECT * FROM items WHERE item_name = ?", (item_name, ))
        item = c.fetchone()
        

        self.text_item_id.setText(str(item[0]))
        self.text_item_name.setText(str(item[1]))
        self.text_item_source_dungeon.setText(str(item[2]))
        self.text_item_slot.setText(str(item[3]))
        self.text_item_source_encounter.setText(str(item[4]))

        # self.filter_tbl_sim_results(str(item[0]),c)

        self.proxy_model.setFilterFixedString(str(item[0]))
        

        conn.commit()
        conn.close()

    #filter tbl_sim_results
    def filter_tbl_sim_results(self, item_id, c):
        
        c.execute("SELECT * FROM sim_results WHERE item_id = ?", (item_id, ))
        item = c.fetchall()
        # print("test")
        # print(item)

    #search button
    def search_items(self):
        search_term = self.text_item_search.text()
        # print(type(search_term))

        conn = sqlite3.connect("whatever.sqlite")
        c = conn.cursor()
        query = '''SELECT * FROM items WHERE item_id = ? OR item_name = ?'''
        c.execute(query, (search_term, search_term))
        item = c.fetchone()
        conn.commit()
        conn.close()
        
        if item is not None:
            matching_item = self.list_items.findItems(item[1], Qt.MatchContains)
        

            if matching_item != None:
                self.list_items.setCurrentItem(matching_item[0])
                self.on_list_item_clicked(matching_item[0])
        if search_term == "":
            self.proxy_model.setFilterFixedString("")
            # self.proxy_model.invalidate()
            self.mod_sim_results.select()

    #close application
    def closeApplication(self):
        QCoreApplication.quit()
    
app = QApplication()
frm_main = Frm_main()
frm_main.show()
app.exec()