# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'frm_main.ui'
##
## Created by: Qt User Interface Compiler version 6.4.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QComboBox, QHeaderView,
    QLabel, QLineEdit, QListWidget, QListWidgetItem,
    QMainWindow, QMenu, QMenuBar, QPushButton,
    QSizePolicy, QStatusBar, QTabWidget, QTableView,
    QTextEdit, QWidget)

class Ui_frm_main(object):
    def setupUi(self, frm_main):
        if not frm_main.objectName():
            frm_main.setObjectName(u"frm_main")
        frm_main.resize(1200, 800)
        self.actionBeenden = QAction(frm_main)
        self.actionBeenden.setObjectName(u"actionBeenden")
        self.centralwidget = QWidget(frm_main)
        self.centralwidget.setObjectName(u"centralwidget")
        self.tabs_main = QTabWidget(self.centralwidget)
        self.tabs_main.setObjectName(u"tabs_main")
        self.tabs_main.setGeometry(QRect(10, 10, 1181, 671))
        self.tab_charaktere = QWidget()
        self.tab_charaktere.setObjectName(u"tab_charaktere")
        self.tbl_charaktere = QTableView(self.tab_charaktere)
        self.tbl_charaktere.setObjectName(u"tbl_charaktere")
        self.tbl_charaktere.setGeometry(QRect(20, 60, 1131, 511))
        self.tbl_charaktere.setStyleSheet(u"")
        self.tbl_charaktere.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.tbl_charaktere.setAlternatingRowColors(True)
        self.tbl_charaktere.setSortingEnabled(True)
        self.lbl_roster = QLabel(self.tab_charaktere)
        self.lbl_roster.setObjectName(u"lbl_roster")
        self.lbl_roster.setGeometry(QRect(20, 20, 61, 21))
        font = QFont()
        font.setPointSize(12)
        self.lbl_roster.setFont(font)
        self.btn_update = QPushButton(self.tab_charaktere)
        self.btn_update.setObjectName(u"btn_update")
        self.btn_update.setGeometry(QRect(490, 580, 91, 41))
        self.btn_update.setFlat(False)
        self.btn_update_sims = QPushButton(self.tab_charaktere)
        self.btn_update_sims.setObjectName(u"btn_update_sims")
        self.btn_update_sims.setGeometry(QRect(600, 580, 91, 41))
        self.btn_update_sims.setFlat(False)
        self.tabs_main.addTab(self.tab_charaktere, "")
        self.tab_items = QWidget()
        self.tab_items.setObjectName(u"tab_items")
        self.ddown_item_filter_dungeon = QComboBox(self.tab_items)
        self.ddown_item_filter_dungeon.setObjectName(u"ddown_item_filter_dungeon")
        self.ddown_item_filter_dungeon.setGeometry(QRect(20, 20, 221, 22))
        self.list_items = QListWidget(self.tab_items)
        self.list_items.setObjectName(u"list_items")
        self.list_items.setGeometry(QRect(20, 110, 221, 511))
        self.text_item_id = QLineEdit(self.tab_items)
        self.text_item_id.setObjectName(u"text_item_id")
        self.text_item_id.setGeometry(QRect(360, 80, 221, 22))
        self.text_item_id.setReadOnly(True)
        self.lbl_item_id = QLabel(self.tab_items)
        self.lbl_item_id.setObjectName(u"lbl_item_id")
        self.lbl_item_id.setGeometry(QRect(270, 80, 81, 22))
        self.lbl_item_name = QLabel(self.tab_items)
        self.lbl_item_name.setObjectName(u"lbl_item_name")
        self.lbl_item_name.setGeometry(QRect(270, 120, 81, 22))
        self.text_item_name = QLineEdit(self.tab_items)
        self.text_item_name.setObjectName(u"text_item_name")
        self.text_item_name.setGeometry(QRect(360, 120, 221, 22))
        self.text_item_name.setReadOnly(True)
        self.text_item_source_dungeon = QLineEdit(self.tab_items)
        self.text_item_source_dungeon.setObjectName(u"text_item_source_dungeon")
        self.text_item_source_dungeon.setGeometry(QRect(360, 200, 221, 22))
        self.text_item_source_dungeon.setReadOnly(True)
        self.lbl_item_slot = QLabel(self.tab_items)
        self.lbl_item_slot.setObjectName(u"lbl_item_slot")
        self.lbl_item_slot.setGeometry(QRect(270, 160, 81, 22))
        self.text_item_slot = QLineEdit(self.tab_items)
        self.text_item_slot.setObjectName(u"text_item_slot")
        self.text_item_slot.setGeometry(QRect(360, 160, 221, 22))
        self.text_item_slot.setReadOnly(True)
        self.lbl_item_source_dungeon = QLabel(self.tab_items)
        self.lbl_item_source_dungeon.setObjectName(u"lbl_item_source_dungeon")
        self.lbl_item_source_dungeon.setGeometry(QRect(270, 200, 81, 22))
        self.lbl_item_source_encounter = QLabel(self.tab_items)
        self.lbl_item_source_encounter.setObjectName(u"lbl_item_source_encounter")
        self.lbl_item_source_encounter.setGeometry(QRect(270, 240, 81, 22))
        self.text_item_source_encounter = QLineEdit(self.tab_items)
        self.text_item_source_encounter.setObjectName(u"text_item_source_encounter")
        self.text_item_source_encounter.setGeometry(QRect(360, 240, 221, 22))
        self.text_item_source_encounter.setReadOnly(True)
        self.ddown_item_filter_encounter = QComboBox(self.tab_items)
        self.ddown_item_filter_encounter.setObjectName(u"ddown_item_filter_encounter")
        self.ddown_item_filter_encounter.setGeometry(QRect(20, 50, 221, 22))
        self.text_item_search = QLineEdit(self.tab_items)
        self.text_item_search.setObjectName(u"text_item_search")
        self.text_item_search.setGeometry(QRect(360, 20, 221, 22))
        self.tbl_sim_results = QTableView(self.tab_items)
        self.tbl_sim_results.setObjectName(u"tbl_sim_results")
        self.tbl_sim_results.setGeometry(QRect(610, 80, 541, 541))
        self.tbl_sim_results.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.tbl_sim_results.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tbl_sim_results.setAlternatingRowColors(True)
        self.tbl_sim_results.setSortingEnabled(True)
        self.btn_item_filter_dungeon_submit = QPushButton(self.tab_items)
        self.btn_item_filter_dungeon_submit.setObjectName(u"btn_item_filter_dungeon_submit")
        self.btn_item_filter_dungeon_submit.setGeometry(QRect(20, 80, 101, 22))
        self.btn_item_filter_encounter_submit = QPushButton(self.tab_items)
        self.btn_item_filter_encounter_submit.setObjectName(u"btn_item_filter_encounter_submit")
        self.btn_item_filter_encounter_submit.setGeometry(QRect(140, 80, 101, 22))
        self.btn_item_search = QPushButton(self.tab_items)
        self.btn_item_search.setObjectName(u"btn_item_search")
        self.btn_item_search.setGeometry(QRect(270, 20, 75, 22))
        self.tabs_main.addTab(self.tab_items, "")
        self.tab_advanced = QWidget()
        self.tab_advanced.setObjectName(u"tab_advanced")
        self.tabs_main.addTab(self.tab_advanced, "")
        self.tab_log = QWidget()
        self.tab_log.setObjectName(u"tab_log")
        self.text_log_viewer = QTextEdit(self.tab_log)
        self.text_log_viewer.setObjectName(u"text_log_viewer")
        self.text_log_viewer.setGeometry(QRect(20, 20, 1131, 601))
        font1 = QFont()
        font1.setFamilies([u"Fira Code"])
        self.text_log_viewer.setFont(font1)
        self.text_log_viewer.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.text_log_viewer.setReadOnly(True)
        self.tabs_main.addTab(self.tab_log, "")
        frm_main.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(frm_main)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1200, 22))
        self.menuDatei = QMenu(self.menubar)
        self.menuDatei.setObjectName(u"menuDatei")
        frm_main.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(frm_main)
        self.statusbar.setObjectName(u"statusbar")
        frm_main.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuDatei.menuAction())
        self.menuDatei.addAction(self.actionBeenden)

        self.retranslateUi(frm_main)

        self.tabs_main.setCurrentIndex(3)


        QMetaObject.connectSlotsByName(frm_main)
    # setupUi

    def retranslateUi(self, frm_main):
        frm_main.setWindowTitle(QCoreApplication.translate("frm_main", u"whatever", None))
        self.actionBeenden.setText(QCoreApplication.translate("frm_main", u"Beenden", None))
        self.lbl_roster.setText(QCoreApplication.translate("frm_main", u"Roster", None))
        self.btn_update.setText(QCoreApplication.translate("frm_main", u"Update Roster", None))
        self.btn_update_sims.setText(QCoreApplication.translate("frm_main", u"Update Sims", None))
        self.tabs_main.setTabText(self.tabs_main.indexOf(self.tab_charaktere), QCoreApplication.translate("frm_main", u"Charaktere", None))
        self.lbl_item_id.setText(QCoreApplication.translate("frm_main", u"ID", None))
        self.lbl_item_name.setText(QCoreApplication.translate("frm_main", u"Name", None))
        self.lbl_item_slot.setText(QCoreApplication.translate("frm_main", u"Slot", None))
        self.lbl_item_source_dungeon.setText(QCoreApplication.translate("frm_main", u"Dungeon", None))
        self.lbl_item_source_encounter.setText(QCoreApplication.translate("frm_main", u"Encounter", None))
        self.btn_item_filter_dungeon_submit.setText(QCoreApplication.translate("frm_main", u"Set Dungeon", None))
        self.btn_item_filter_encounter_submit.setText(QCoreApplication.translate("frm_main", u"Set Encounter", None))
        self.btn_item_search.setText(QCoreApplication.translate("frm_main", u"Suche", None))
        self.tabs_main.setTabText(self.tabs_main.indexOf(self.tab_items), QCoreApplication.translate("frm_main", u"Items", None))
        self.tabs_main.setTabText(self.tabs_main.indexOf(self.tab_advanced), QCoreApplication.translate("frm_main", u"Advanced", None))
        self.tabs_main.setTabText(self.tabs_main.indexOf(self.tab_log), QCoreApplication.translate("frm_main", u"Log", None))
        self.menuDatei.setTitle(QCoreApplication.translate("frm_main", u"Datei", None))
    # retranslateUi

