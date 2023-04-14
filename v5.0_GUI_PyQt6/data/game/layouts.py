import sys, os, random, itertools, re

from data.db.db import *

from PyQt6.QtWidgets import QMainWindow, QApplication, QWidget, QVBoxLayout, QGridLayout, QLabel, QGraphicsScene, QGraphicsView, QPushButton, QSizePolicy, QHBoxLayout, QMenuBar, QMenu, QSpinBox, QLineEdit, QStackedWidget, QStackedLayout, QInputDialog, QMessageBox, QTableWidget,QTableWidgetItem
from PyQt6.QtGui import QPixmap, QIcon, QImage, QBrush, QFont, QPainter, QAction
from PyQt6.QtCore import QSize, Qt, QRectF, QTimer, QFileInfo, QBuffer, QCoreApplication, QUrlQuery
from PyQt6.QtSql import QSqlDatabase, QSqlQuery
from PyQt6 import QtCore, QtGui
from PyQt6.QtCore import QUrl
from PyQt6.QtMultimedia import QSoundEffect

# HIGH SCORES layout
def layout_high_scores(self):
    self.high_scores_layout = QVBoxLayout()        
    self.high_scores_table = QTableWidget()
    # self.high_scores_layout.setContentsMargins(100, 10, 100, 10)
    self.high_scores_table.setObjectName('high_scores_table')
    self.high_scores_table.setColumnCount(6)
    column_names = labels()
    self.high_scores_table.setHorizontalHeaderLabels(column_names)
    datas = read_high_scores()
    self.high_scores_table.setRowCount(len(datas))
    self.high_scores_table.setSortingEnabled(True)
    
    for row, data in enumerate(datas):
        for column, value in enumerate(data.values()):
            item = QTableWidgetItem(str(value))
            self.high_scores_table.setItem(row, column, item)
    
    self.back_button = QPushButton('<- Back', clicked=lambda: self.switch_layouts("<- Back"))
    self.reset_button = QPushButton("Reset High Scores", clicked=lambda: self.reply(reset_high_scores, 'Reset High Scores.', 'Are you sure You want to DELETE high scores? '))
    self.buttons(self.reset_button)
    self.buttons(self.back_button)
    self.high_scores_layout.addWidget(QLabel('High Scores'))
    self.high_scores_layout.addWidget(self.high_scores_table)
    self.high_scores_layout.addWidget(self.reset_button)
    self.high_scores_layout.addWidget(self.back_button)

# RULES layout
def layout_rules(self):
    self.rules_layout = QVBoxLayout()
    self.back_button = QPushButton('<- Back', clicked=lambda: self.switch_layouts("<- Back"))
    self.buttons(self.back_button)
    self.rules_layout.addWidget(QLabel('Zasady gry....'))
    self.rules_layout.addWidget(self.back_button)

# ABOUT layout
def layout_about(self):
    self.about_layout = QVBoxLayout()
    self.back_button = QPushButton('<- Back', clicked=lambda: self.switch_layouts("<- Back"))
    self.buttons(self.back_button)
    self.about_layout.addWidget(QLabel('O grze...'))
    self.about_layout.addWidget(self.back_button)
