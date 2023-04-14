import sys, os, random, itertools, re
from math import ceil

from data.db.db import *
# from data.db import db
from data.game.layouts import layout_high_scores, layout_rules, layout_about

from PyQt6.QtWidgets import QMainWindow, QApplication, QWidget, QVBoxLayout, QGridLayout, QLabel, QGraphicsScene, QGraphicsView, QPushButton, QSizePolicy, QHBoxLayout, QMenuBar, QMenu, QSpinBox, QLineEdit, QStackedWidget, QStackedLayout, QInputDialog, QMessageBox, QTableWidget,QTableWidgetItem, QLayout, QBoxLayout, QGroupBox, QStyle, QTextEdit
from PyQt6.QtGui import QPixmap, QIcon, QImage, QBrush, QFont, QPainter, QAction, QCursor, QPalette, QColor, QTextCursor
from PyQt6.QtCore import QSize, Qt, QRectF, QTimer, QFileInfo, QBuffer, QCoreApplication, QUrlQuery, QRect
from PyQt6.QtSql import QSqlDatabase, QSqlQuery
from PyQt6 import QtCore, QtGui
from PyQt6.QtCore import QUrl, QMargins
from PyQt6.QtMultimedia import QSoundEffect


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # making datebase
        create_db()
        # making new tables, default
        game_statistics_table_default()
        high_scores_table_default()
        self.initUI()
    
    def initUI(self):
        # main window settings
        self.setWindowTitle('Battle Ships v5.0')
        self.setWindowIcon(QIcon(r'data/images/main/fav.png'))
        
        # MENUBAR        
        self.menu_bar = QMenuBar(self) # making menu bar
        self.menu_bar.setObjectName("menu_bar")
        self.setMenuBar(self.menu_bar)
        self.menu_game = QMenu("Game", self.menu_bar) # making menu
        self.menu_game.setObjectName("menu_game")
        self.menu_help = QMenu("Help", self.menu_bar)
        self.menu_help.setObjectName("menu_help")
        self.menu_bar.addMenu(self.menu_game)
        self.menu_bar.addMenu(self.menu_help)        
        self.action_high_scores = QAction("High Scores", self)
        self.action_high_scores.setObjectName('high_scores')
        self.action_high_scores.setIcon(QIcon(r"data/images/main/top10.png"))
        self.action_high_scores.triggered.connect(lambda: self.switch_layouts("High Scores"))        
        self.action_exit = QAction("Exit", self) # making element of action
        self.action_exit.setObjectName('action_exit')
        self.action_exit.setIcon(QIcon(r"data/images/main/exit.png"))
        self.action_exit.triggered.connect(self.close)        
        self.action_rules = QAction("Rules", self)
        self.action_rules.setIcon(QIcon(r"data/images/main/rules.png"))
        self.action_rules.triggered.connect(lambda: self.switch_layouts("Rules"))        
        self.action_about = QAction("About", self) # making action        
        self.action_about.setIcon(QIcon(r"data/images/main/fav.png"))
        self.action_about.triggered.connect(lambda: self.switch_layouts("About"))
        
        # adding action of element to menu
        self.menu_game.addAction(self.action_high_scores)
        self.menu_game.addSeparator()
        self.menu_game.addAction(self.action_exit)
        self.menu_help.addAction(self.action_rules)
        self.menu_help.addAction(self.action_about) 
        
        # CENTRAL widget
        self.central_widget = QWidget()
        self.central_widget.setObjectName('central_widget')
        
        # PLAYER widget
        self.player_widget = QWidget(parent=self.central_widget)
        self.player_widget.setObjectName('player_widget')
        self.player_widget.setMaximumSize(350, 600)
        self.widget = QWidget(self.player_widget)
        self.player_widget_layout = QVBoxLayout(self.widget)
        # name
        self.player_name = QLabel("Player", self.widget)        
        self.player_name.setContentsMargins(20, 5, 10, 5) 
        self.player_name.setFont(QFont("Arial", 12))
        self.player_widget_layout.addWidget(self.player_name, 0, QtCore.Qt.AlignmentFlag.AlignHCenter|QtCore.Qt.AlignmentFlag.AlignVCenter)
        # making player board
        self.player_board_layout =  QGridLayout()
        self.player_board_layout.setSpacing(0)
        self.player_board = self.sea_zone(self.player_board_layout)
        self.player_widget_layout.addLayout(self.player_board_layout)
        # statistics
        self.player_statistics_layout = QVBoxLayout()
        self.player_statistics_layout.setContentsMargins(10, 5, 10, 5) 
        self.player_statistic_1 = QLabel("Ships", self.player_widget)
        self.player_statistic_1.setObjectName('player_statistic_1')
        self.player_statistics_layout.addWidget(self.player_statistic_1)
        self.player_statistic_2 = QLabel("Avaiable Shots", self.player_widget)
        self.player_statistics_layout.addWidget(self.player_statistic_2)
        self.player_statistic_3 = QLabel("Shots (All)", self.player_widget)
        self.player_statistics_layout.addWidget(self.player_statistic_3)
        self.player_statistic_4 = QLabel("Hit shots", self.player_widget)
        self.player_statistics_layout.addWidget(self.player_statistic_4)
        self.player_statistic_5 = QLabel("Missed shots", self.player_widget)
        self.player_statistics_layout.addWidget(self.player_statistic_5)
        self.player_statistic_6 = QLabel("Effective", self.player_widget)
        self.player_statistics_layout.addWidget(self.player_statistic_6)
        self.player_widget_layout.addLayout(self.player_statistics_layout)
        # actions
        self.player_actions = QLabel("Actions", self.widget)        
        self.player_actions.setContentsMargins(10, 5, 10, 5) 
        self.player_widget_layout.addWidget(self.player_actions)        
        self.player_widget.setLayout(self.player_widget_layout)
        
        # CPU widget
        self.cpu_widget = QWidget(parent=self.central_widget)
        self.cpu_widget.setObjectName('cpu_widget')
        self.cpu_widget.setMaximumSize(350, 600)
        self.widget1 = QWidget(self.cpu_widget)
        self.cpu_widget_layout = QVBoxLayout(self.widget1)
        # name
        self.cpu_name = QLabel("CPU", self.widget1)
        self.cpu_name.setContentsMargins(20, 5, 10, 5) 
        self.cpu_name.setFont(QFont("Arial", 12))
        self.cpu_widget_layout.addWidget(self.cpu_name, 0, QtCore.Qt.AlignmentFlag.AlignHCenter|QtCore.Qt.AlignmentFlag.AlignVCenter)
        # making player board
        self.cpu_board_layout =  QGridLayout()
        self.cpu_board_layout.setSpacing(0)
        self.cpu_board = self.sea_zone(self.cpu_board_layout)
        self.cpu_widget_layout.addLayout(self.cpu_board_layout)
        # statistics
        self.cpu_statistics_layout = QVBoxLayout()
        self.cpu_statistics_layout.setContentsMargins(10, 5, 10, 5)        
        self.cpu_statistic_1 = QLabel("Stat 1", self.widget1)
        self.cpu_statistic_1.setObjectName('player_statistic_1')
        self.cpu_statistics_layout.addWidget(self.cpu_statistic_1)
        self.cpu_statistic_2 = QLabel("Stat 2", self.widget1)
        self.cpu_statistics_layout.addWidget(self.cpu_statistic_2)
        self.cpu_statistic_3 = QLabel("Stat 3", self.widget1)
        self.cpu_statistics_layout.addWidget(self.cpu_statistic_3)
        self.cpu_statistic_4 = QLabel("Stat 4", self.widget1)
        self.cpu_statistics_layout.addWidget(self.cpu_statistic_4)
        self.cpu_statistic_5 = QLabel("Stat 5", self.widget1)
        self.cpu_statistics_layout.addWidget(self.cpu_statistic_5)
        self.cpu_statistic_6 = QLabel("Effective", self.widget1)
        self.cpu_statistics_layout.addWidget(self.cpu_statistic_6)
        self.cpu_widget_layout.addLayout(self.cpu_statistics_layout)
        # actions
        self.cpu_actions = QLabel("Actions", self.widget1)        
        self.cpu_actions.setContentsMargins(10, 5, 10, 5)      
        self.cpu_widget_layout.addWidget(self.cpu_actions)
        self.cpu_widget.setLayout(self.cpu_widget_layout)
        self.stat()
        
        # MENU container
        self.menu_widget = QWidget(self.central_widget)
        self.menu_widget.setObjectName('menu_widget')
        self.menu_widget.setMaximumSize(200, 300)        
        self.widget3 = QWidget(self.menu_widget)        
        self.menu_container_layout = QVBoxLayout(self.widget3)
        # making main menu buttons
        self.main_menu_zone()
        self.menu_widget.setLayout(self.menu_container_layout)
        self.menu_container_layout.setSpacing(0)        
        
        # set in horizontal PLAYER and CPU widgets. MAIN LAYOUT
        self.main_layout = QHBoxLayout()
        self.main_layout.addWidget(self.player_widget)
        self.main_layout.addWidget(self.cpu_widget)
        self.main_layout.addWidget(self.menu_widget)       
        
        # HIGH SCORES layout
        self.high_scores_layout = QVBoxLayout()
        self.high_scores_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.high_scores_table = QTableWidget()
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
        self.reset_button = QPushButton("Reset High Scores", clicked=lambda: self.reply(reset_high_scores, 'RESET High Scores!', 'Are you sure You want to DELETE high scores?? '))
        self.buttons(self.reset_button)
        self.buttons(self.back_button)
        self.high_scores_layout.addWidget(QLabel('high_scores....'))
        self.high_scores_layout.addWidget(self.high_scores_table)
        self.high_scores_layout.addWidget(self.reset_button)
        self.high_scores_layout.addWidget(self.back_button)
        # layout_high_scores(self)
        
        # RULES layout
        self.rules_layout = QVBoxLayout()
        rules = {'title': QLabel('Battle Ships v5.0'),
                'rules': QLabel('Rules Game: v5.0'),
                'amount ships (default)': QLabel('4'),
                'max ships': QLabel('10'),
                'amount ships (default)': QLabel('4'),
                'level (default)': QLabel('Normal'),
                'difficulty levels': QLabel('Easy, Normal, Hard'),
                'level rules - easy': QLabel('Player +1 ship'),
                'level rules - hard': QLabel('CPU +1 ship'),
                'Available shots': QLabel('Active ships / 2'),
                'Ship by Ship': QLabel('No')
            }
        self.back_button = QPushButton('<- Back', clicked=lambda: self.switch_layouts("<- Back"))
        self.buttons(self.back_button)
        self.descriptions(rules, self.rules_layout)
        self.rules_layout.addWidget(self.back_button)
        # layout_rules(self)
        
        # ABOUT layout
        self.about_layout = QVBoxLayout()
        self.back_button = QPushButton('<- Back', clicked=lambda: self.switch_layouts("<- Back"))
        self.buttons(self.back_button)
        self.about = {
            'name': QLabel('Battle Ships v5.0'),
            'date': QLabel('April 12th, 2023'),
            'author': QLabel('Lukasz Szabat'),
            'email': QLabel('synvoret@gmail.com')
        }        
        self.descriptions(self.about, self.about_layout)
        self.about_layout.addWidget(self.back_button)
        # layout_about(self)
        
        # STACKED layouts
        self.stacked_layout = QStackedLayout(self.central_widget)
        for i in range(4):
            widget = QWidget()
            widget.setMaximumSize(900, 650)
            x = (self.width() - widget.width()) // 2
            y = (self.height() - widget.height()) // 2
            widget.setGeometry(x, y, widget.width(), widget.height())
            self.stacked_layout.addWidget(widget)
        self.stacked_layout.widget(0).setLayout(self.main_layout)
        self.stacked_layout.widget(1).setLayout(self.about_layout)
        self.stacked_layout.widget(2).setLayout(self.rules_layout)
        self.stacked_layout.widget(3).setLayout(self.high_scores_layout)        
        self.stacked_layout.maximumSize()
        
        self.setCentralWidget(self.central_widget)
        self.centralWidget().setLayout(self.stacked_layout)
        self.centralWidget().setContentsMargins(50, 25, 50, 25)
    
    def stat(self):
        '''Method responsible for refreshing statistics displayed on the screen.'''
        
        self.player_statistic_1.setText(f"Ships: {get_value_from_game_statistics('player_ships')}")
        self.player_statistic_2.setText(f"Available Shots: {get_value_from_game_statistics('player_available_shots')}")
        self.player_statistic_3.setText(f"Shots (All): {get_value_from_game_statistics('player_shots')}")
        self.player_statistic_4.setText(f"Hit Shots: {get_value_from_game_statistics('player_hit')}")
        self.player_statistic_5.setText(f"Missed Shots: {get_value_from_game_statistics('player_missed')}")
        self.player_statistic_6.setText(f"Effective: {get_value_from_game_statistics('player_effective')}")

        self.cpu_statistic_1.setText(f"Ships: {get_value_from_game_statistics('cpu_ships')}")
        self.cpu_statistic_2.setText(f"Available Shots: {get_value_from_game_statistics('cpu_available_shots')}")
        self.cpu_statistic_3.setText(f"Shots (All): {get_value_from_game_statistics('cpu_shots')}")
        self.cpu_statistic_4.setText(f"Hit Shots: {get_value_from_game_statistics('cpu_hit')}")
        self.cpu_statistic_5.setText(f"Missed Shots: {get_value_from_game_statistics('cpu_missed')}")
        self.cpu_statistic_6.setText(f"Effective: {get_value_from_game_statistics('cpu_effective')}")
    
    def switch_layouts(self, _from):
        '''Method responsible for switching beetwen layouts.'''
        if _from == "<- Back":
            self.stacked_layout.setCurrentWidget(self.stacked_layout.widget(0))
        elif _from == "About":
            self.stacked_layout.setCurrentWidget(self.stacked_layout.widget(1))
        elif _from == "Rules":
            self.stacked_layout.setCurrentWidget(self.stacked_layout.widget(2))
        elif _from == "High Scores":
            self.stacked_layout.setCurrentWidget(self.stacked_layout.widget(3))
    
    def descriptions(self, d: dict, layout):
        for item in d.items():
            line = QHBoxLayout()
            title = item[0].title()
            title_text = item[1].text()
            text = QLabel(f"{title}: {title_text}")
            text.setAlignment(Qt.AlignmentFlag.AlignCenter)
            text.setObjectName('text')
            text.setFont(QFont('Arial', 12))
            line.addWidget(text)
            layout.addLayout(line)
    
    def buttons(self, button):
        button.setObjectName('button')
        button.setFixedSize(130, 30)
        button.setFont(QFont("Arial", 10))
        button.enterEvent = lambda event, btn=button: btn.setFont(QFont("Arial", 10, italic=True))
        button.leaveEvent = lambda event, btn=button: btn.setFont(QFont("Arial", 9))
        if button.text() == '':
            button.setEnabled(False)
    
    def reply(self, func, title, message):
        '''Method that requires confirmation to perform a specific task.'''
        sound = QSoundEffect()
        try:
            sound.setSource(QUrl.fromLocalFile("C:/Windows/Media/Windows Critical Stop.wav"))
            sound.play()
        except:
            pass
        reply = QMessageBox.warning(self, f"{title}", f"{message}", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            func()
    
    def sea_zone(self, who_grid):
        '''Method responsible for creating a clean board for selected side.'''
        board = []
        self.sea_image = QPixmap('data\images\game\sea.png').scaled(QSize(30, 30))
        self.sea_icon = QIcon(self.sea_image)
        for i in range(10):
            row = []
            for j in range(10):
                locals()['btn{i}{j}'] = row.append(QPushButton(parent=self.widget))
                btn = row[int(f"{j}")]
                btn.setStyleSheet("background-color: rgb(200, 200, 200)")
                btn.setMouseTracking(True)
                btn.setIcon(self.sea_icon)
                btn.setIconSize(QSize(30, 30))
                # btn.enterEvent = lambda event, btn=btn: btn.setStyleSheet("background-color: #00C6F7")
                # btn.leaveEvent = lambda event, btn=btn: btn.setStyleSheet("background-color: rgb(200, 200, 200)")
                btn.setEnabled(False)
                who_grid.addWidget(btn, i, j)
            board.extend(row)
        return board
    
    def main_menu_zone(self):
        '''Method responsible for displaying the main menu buttons.'''
        self.main_menu_list = [
            (QPushButton("Start Battle", self), self.start_battle),
            (QPushButton("Player Fleet", self), self.player_fleet),
            (QPushButton("Random Fleets", self), lambda: [self.random_fleet('player'), self.random_fleet('cpu')]),
            (QPushButton("Clear Player Board", self), self.clear_player_board),
            (QPushButton("Setup Game", self), self.setup_menu),
            (QPushButton("Reset Game", self), self.reset_game),
            (QPushButton("Quit Game", self), self.close)
        ]
        if self.menu_container_layout.count() != 0:
            for button in self.main_menu_list:
                widget = self.menu_container_layout.itemAt(0).widget()
                self.menu_container_layout.removeWidget(widget)
                widget.setParent(None)
                self.menu_container_layout.addWidget(button[0])                
                try:
                    button[0].clicked.disconnect()
                except TypeError:
                    pass
                button[0].clicked.connect(button[1])
                self.buttons(button[0])
        else:
            for button in self.main_menu_list:
                self.menu_container_layout.addWidget(button[0])
                try:
                    button[0].clicked.disconnect()
                except TypeError:
                    pass
                button[0].clicked.connect(button[1])
                self.buttons(button[0])
        
        for i in range(0, len(self.player_board)):
            self.player_board[i].setEnabled(False)
            self.cpu_board[i].setEnabled(False)
    
    def player_turn(self):
        player_available_shots = ceil(get_value_from_game_statistics('player_ships') * 0.5) # tworzę ilośc dostępnych strzałów w turze gracza
        update_game_statistics_table('player_available_shots', player_available_shots) # aktualizuje dane w bazie danych
        self.stat()
        calculate_value_from_game_statistic('turns', 1)
        if get_value_from_game_statistics('player_ships') == 0:
            self.end_game('cpu')
            return
        for i in range(0, len(self.cpu_board)):
            try:
                self.cpu_board[i].clicked.disconnect()
            except TypeError:
                pass
            self.cpu_board[i].clicked.connect(lambda checked, button=self.cpu_board[i]: [self.shot('player', self.cpu_board.index(button))])
    
    def cpu_turn(self):
        cpu_avaiable_shots = ceil(get_value_from_game_statistics('cpu_ships') * 0.5)
        update_game_statistics_table('cpu_available_shots', cpu_avaiable_shots)
        if get_value_from_game_statistics('cpu_ships') == 0:
            self.end_game('player')
            return
        i = 0 # zliczanie oddanych strzałów
        i_max = get_value_from_game_statistics('cpu_available_shots') # maksymalna ilość strzałów w turze
        while i < i_max:
            zone = random.randint(0, len(self.player_board) - 1) # losuję strefę w która strzela
            if str(zone) in get_zones('shot') or str(zone) in get_zones('fire'):
                continue
            update_zones('shot', zone)
            i += 1
            self.shot('cpu', zone)
        self.stat()
        self.player_turn()
    
    def check_coordinate(self, who: str, checking_zone: int, move: str):
        '''Method validates the selected zone depending on the situation. The main assumptions are: the ship cannot stand next to the ship. Return 'bool'.'''
        
        # cases of zones
        top_left_corner = (1, 10, 11)  # if zone 0
        top_side = (-1, 1, 9, 10, 11 ) # if zones from 1 to 8 every 1
        top_right_corner = (-1, 9, 10)  # if zone 9
        right_side = (-11, -10, -1, 9, 10)  # if zones from 19 to 89 every 10
        bottom_right_corner = (-11, -10, -1 ) # if zone 99
        bottom_side = (-11, -10, -9, -1, 1)  # if zones from 91 to 98 every 1
        bottom_left_corner = (-10, -9, 1)  # if zone 90
        left_side = (-10, -9, 1, 10, 11)  # if zones from 10 to 80 every 10
        inside = (-11, -10, -9, -1, 1, 9, 10, 11)  # if rest of cases
        # zones = {
        #     "top_left_corner": 0, # zone 0
        #     "top_side": tuple(i for i in range(1, 9)),  # zone from 1 to 8 every 1
        #     "top_right_corner": 9, # zone 9
        #     "right_side": tuple(i for i in range(19, 90, 10)), # zone from 19 to 89 every 10
        #     "bottom_right_corner": 99, # zone 99
        #     "bottom_side": tuple(i for i in range(91, 99, 1)), # zone from 91 to 98 every 1
        #     "bottom_left_corner": 90, # zone 90
        #     "left_side": tuple(i for i in range(10, 81, 10)), # zone from 10 to 80 every 10
        #     "inside": {i + j for i in range(10, 81, 10) for j in range(1, 9)}, # rest of cases zones
        # }
        
        # board
        if who == 'player':
            self.board = self.player_board
            self.action = self.player_actions
        elif who == 'cpu':
            self.board == self.cpu_board
            self.action = self.cpu_actions
            print(f'stawiam w strefie {checking_zone}')
        
        # in SENDING ships (move = 'ship')
        if checking_zone == 0:
            for i in top_left_corner:
                if self.board[checking_zone + i].icon().pixmap(self.board[checking_zone + i].icon().availableSizes()[0]).toImage() == self.ship_image.toImage():
                    print(f'{checking_zone} Too close ship in {checking_zone + i} zone')
                    # self.action.setText('Too close another Ship!')
                    return False
        elif checking_zone in tuple(range(1, 9)):
            for i in top_side:
                if self.board[checking_zone + i].icon().pixmap(self.board[checking_zone + i].icon().availableSizes()[0]).toImage() == self.ship_image.toImage():
                    print(f'{checking_zone} Too close ship in {checking_zone + i} zone')
                    return False
        elif checking_zone == 9:
            for i in top_right_corner:
                if self.board[checking_zone + i].icon().pixmap(self.board[checking_zone + i].icon().availableSizes()[0]).toImage() == self.ship_image.toImage():
                    print(f'{checking_zone} Too close ship in {checking_zone + i} zone')
                    return False
        elif checking_zone in tuple(range(19, 90, 10)):
            for i in right_side:
                if self.board[checking_zone + i].icon().pixmap(self.board[checking_zone + i].icon().availableSizes()[0]).toImage() == self.ship_image.toImage():
                    print(f'{checking_zone} Too close ship in {checking_zone + i} zone')
                    return False
        elif checking_zone == 99:
            for i in bottom_right_corner:
                if self.board[checking_zone + i].icon().pixmap(self.board[checking_zone + i].icon().availableSizes()[0]).toImage() == self.ship_image.toImage():
                    print(f'{checking_zone} Too close ship in {checking_zone + i} zone')
                    return False
        elif checking_zone in tuple(range(91, 99)):
            for i in bottom_side:
                if self.board[checking_zone + i].icon().pixmap(self.board[checking_zone + i].icon().availableSizes()[0]).toImage() == self.ship_image.toImage():
                    print(f'{checking_zone} Too close ship in {checking_zone + i} zone')
                    return False
        elif checking_zone == 90:
            for i in bottom_left_corner:
                if self.board[checking_zone + i].icon().pixmap(self.board[checking_zone + i].icon().availableSizes()[0]).toImage() == self.ship_image.toImage():
                    print(f'{checking_zone} Too close ship in {checking_zone + i} zone')
                    return False
        elif checking_zone in tuple(range(10, 81, 10)):
            for i in left_side:
                if self.board[checking_zone + i].icon().pixmap(self.board[checking_zone + i].icon().availableSizes()[0]).toImage() == self.ship_image.toImage():
                    print(f'{checking_zone} Too close ship in {checking_zone + i} zone')
                    return False
        else:
            for i in inside:
                if self.board[checking_zone + i].icon().pixmap(self.board[checking_zone + i].icon().availableSizes()[0]).toImage() == self.ship_image.toImage():
                    print(f'{checking_zone} Too close ship in {checking_zone + i} zone')
                    return False
    
    def shot(self, who: str, zone: int):
        calculate_value_from_game_statistic(f"{who}_shots", 1)
        calculate_value_from_game_statistic(f"{who}_available_shots", -1)
        if who == 'player':
            if self.cpu_board[zone].icon().pixmap(self.cpu_board[zone].icon().availableSizes()[0]).toImage() == self.ship_image.toImage():
                self.cpu_board[zone].setIcon(self.fired_icon)
                calculate_value_from_game_statistic(f"player_hit", 1)
                calculate_value_from_game_statistic(f"cpu_ships", -1)
            elif self.cpu_board[zone].icon().pixmap(self.cpu_board[zone].icon().availableSizes()[0]).toImage() == self.sea_image.toImage():
                self.cpu_board[zone].setIcon(self.missed_icon)
                calculate_value_from_game_statistic(f"player_missed", 1)
            elif self.cpu_board[zone].icon().pixmap(self.cpu_board[zone].icon().availableSizes()[0]).toImage() == self.fired_image.toImage():
                calculate_value_from_game_statistic(f"{who}_missed", 1)
            elif self.cpu_board[zone].icon().pixmap(self.cpu_board[zone].icon().availableSizes()[0]).toImage() == self.missed_image.toImage():
                calculate_value_from_game_statistic(f"{who}_missed", 1)
            if get_value_from_game_statistics(f"player_available_shots") == 0: # sprawdzam czy są dostępne strzały
                self.cpu_turn()
        elif who == 'cpu':
            if self.player_board[zone].icon().pixmap(self.player_board[zone].icon().availableSizes()[0]).toImage() == self.sea_image.toImage():
                self.player_board[zone].setIcon(self.missed_icon)
                calculate_value_from_game_statistic(f"{who}_missed", 1)
            elif self.player_board[zone].icon().pixmap(self.player_board[zone].icon().availableSizes()[0]).toImage() == self.ship_image.toImage():
                self.player_board[zone].setIcon(self.fired_icon)
                calculate_value_from_game_statistic(f"{who}_hit", 1)
                calculate_value_from_game_statistic(f"player_ships", -1)
            elif self.player_board[zone].icon().pixmap(self.player_board[zone].icon().availableSizes()[0]).toImage() == self.fired_image.toImage():
                calculate_value_from_game_statistic(f"{who}_missed", 1)
            elif self.player_board[zone].icon().pixmap(self.player_board[zone].icon().availableSizes()[0]).toImage() == self.missed_image.toImage():
                calculate_value_from_game_statistic(f"{who}_missed", 1)
        
        self.stat()
    
    def end_game(self, winner: str):
        for i in range(0, len(self.cpu_board)):
            try:
                self.cpu_board[i].clicked.disconnect()
            except TypeError:
                pass
        self.stat()
        self.end_game_menu_list = [
            (QPushButton(""), lambda: None),
            (QPushButton("Retreat"), lambda: None),
            (QPushButton(""), lambda: None),
            (QPushButton(""), lambda: None),
            (QPushButton(""), lambda: None),
            (QPushButton(""), lambda: None),
            (QPushButton("<- Back to Menu", self), self.main_menu_zone)
        ]
        try:
            self.end_game_menu_list[1][0].clicked.disconnect().setEnabled(False)
        except TypeError:
            pass
        self.menu_zone(self.end_game_menu_list)
        turns = get_value_from_game_statistics('turns')
        message = get_value_from_game_statistics(f"{winner}_name") + f" won after {turns} turns!"
        
        # wrzucam high scorsy
        player_name = get_value_from_game_statistics(f"{winner}_name")
        effective = get_value_from_game_statistics(f"{winner}_effective")
        game_time = '120 s'
        date = '2023-04-13'
        add_high_scores(player_name, effective, turns, game_time, date)
        self.player_actions.setText(message)
    
    def start_battle(self):
        statistics_to_restart = [
            'turns', 
            'player_available_shots', 
            'player_missed', 
            'player_hit', 
            'player_shots', 
            'cpu_shots', 
            'cpu_available_shots', 
            'cpu_missed', 
            'cpu_hit', 
            'cpu_shots', 
            'shot_zones'
            ]
        for statistic in statistics_to_restart:
            if statistic != 'shot_zones':
                update_game_statistics_table(statistic, 0)
            elif statistic == 'shot_zones':
                update_zones('shot', '-')
        # to_restart_memory_player_board = self.player_board
        if get_value_from_game_statistics('player_ships') != self.level_game('player') or get_value_from_game_statistics('cpu_ships') != self.level_game('cpu'):
            if get_value_from_game_statistics('player_ships') != self.level_game('player'):
                self.player_actions.setText('graczu, masz za mało statków')
            if get_value_from_game_statistics('cpu_ships') != self.level_game('cpu'):
                self.cpu_actions.setText('komputer ma za mało statków')
            return False
        else:
            self.player_actions.setText('Destroy Your Enemy!!! Shoot!')
            self.cpu_actions.setText('CPU shoots!!')
        
        def retreat(back_to_menu_zone=None):
            if back_to_menu_zone:
                pass
            else:
                self.sea_zone(self.player_board_layout)
                update_game_statistics_table('player_ships', 0)
            for i in range(0, len(self.cpu_board)):
                self.cpu_board[i].setEnabled(False)
            self.stat()
        
        start_battle_list = [
                (QPushButton(""), lambda: None),
                (QPushButton("Retreat"), retreat),
                (QPushButton(""), lambda: None),
                (QPushButton(""), lambda: None),
                (QPushButton(""), lambda: None),
                (QPushButton(""), lambda: None),
                (QPushButton("<- Back to Menu", self), lambda: [self.main_menu_zone(), retreat(back_to_menu_zone=True)])
            ]
        self.menu_zone(start_battle_list)
        for i in range(0, len(self.player_board)):
            self.player_board[i].setEnabled(True)
            self.cpu_board[i].setEnabled(True)
        self.player_turn() # kto zaczyna grę
        self.stat()
    
    def player_fleet(self):
        '''Method responsible for manually placing ships on the player board.'''
        self.player_fleet_menu_list = [
            (QPushButton(""), lambda: None),
            (QPushButton(""), lambda: None),
            (QPushButton(""), lambda: None),
            (QPushButton(""), lambda: None),
            (QPushButton(""), lambda: None),
            (QPushButton(""), lambda: None),
            (QPushButton("<- Back to Menu", self), self.main_menu_zone)
        ]
        self.menu_zone(self.player_fleet_menu_list)        
        for i in range(0, len(self.player_board)):
            self.player_board[i].setEnabled(True)
            try:
                self.player_board[i].clicked.disconnect()
            except TypeError:
                pass
            self.player_board[i].clicked.connect(lambda x=self.player_board[i], y=i, z=4: [self.ship('player', y, z), self.stat()]) # x - button, y - index on the list, z - amount of ships
    
    def ship(self, who: str, zone: int, *args: int):
        '''Method responsible for the correct placement of ships an the board.'''
        self.ship_image = QPixmap(r'data/images/game/ship1.png').scaled(QSize(30, 30))
        self.ship_icon = QIcon(self.ship_image)
        self.missed_image = QPixmap(r'data/images/game/missed1.png').scaled(QSize(30, 30))
        self.missed_icon = QIcon(self.missed_image)
        self.fired_image = QPixmap(r'data/images/game/fire1.png').scaled(QSize(30, 30))
        self.fired_icon = QIcon(self.fired_image)
        
        if self.check_coordinate(who, zone, "ship") == False:
            return
        
        def placement(btn):
            '''Internal function of the ship() method that checks currently selected sea zone.'''
            if btn.icon().pixmap(btn.icon().availableSizes()[0]).toImage() == self.sea_image.toImage():  # check actual image
                btn.setIcon(QIcon(self.ship_image))  # change image
                calculate_value_from_game_statistic(f"{who}_ships", 1)
            elif btn.icon().pixmap(btn.icon().availableSizes()[0]).toImage() == self.ship_image.toImage(): # check actual image
                btn.setIcon(QIcon(self.sea_image))  # change image
                calculate_value_from_game_statistic(f"{who}_ships", -1)
        
        if who == 'player':
            btn = self.player_board[zone]
            placement(btn)
        elif who == 'cpu':
            btn = self.cpu_board[zone]
            placement(btn)
    
    def random_fleet(self, who: str):
        '''Method responsible for randomly placing ships on boards of both sides.'''
        while get_value_from_game_statistics(f'{who}_ships') < self.level_game(who):
            random_zone = random.randint(0, 99)
            if who == 'player':
                self.ship('player', random_zone)
            elif who == 'cpu':
                self.ship('cpu', random_zone)
        self.stat()
    
    def clear_player_board(self):
        '''Method clear the player's board.'''
        for zone in self.player_board:
            zone.setIcon(QIcon(self.sea_image))
        update_game_statistics_table('player_ships', 0)
        self.stat()
    
    def menu_zone(self, menu_list: list):
        for button in menu_list:
            widget = self.menu_container_layout.itemAt(0).widget()
            self.menu_container_layout.removeWidget(widget)
            widget.setParent(None)
            self.menu_container_layout.addWidget(button[0])
            if isinstance(button[0], QPushButton):
                try:
                    button[0].clicked.disconnect()
                except TypeError:
                    pass
                button[0].clicked.connect(button[1])
                self.buttons(button[0])
    
    def level_game(self, who: str):
        level = get_value_from_game_statistics('level')
        max_ships = get_value_from_game_statistics('all_ships')
        if level == "Normal":
            return max_ships
        elif level == "Easy":
            player_max_ships = max_ships + 1
            cpu_max_ships = max_ships
            if who == 'player':
                return player_max_ships
            elif who == 'cpu':
                return cpu_max_ships
        elif level == "Hard":
            player_max_ships = max_ships
            cpu_max_ships = max_ships + 1
            if who == 'player':
                return player_max_ships
            elif who == 'cpu':
                return cpu_max_ships
    
    def setup_menu(self):
        '''Method responsible for accessing setup menu board.'''
        
        def player_name_value():
            entry_name = get_value_from_game_statistics('player_name')
            entry_name_line_edit = QLineEdit()
            entry_name_line_edit.setPlaceholderText("Your Name...")            
            entry_name_line_edit.setAlignment(Qt.AlignmentFlag.AlignCenter)
            entry_name_line_edit.setFocus()
            entry_name_line_edit.setMaxLength(10)
            entry_name_line_edit.setFixedSize(130, 30)
            entry_name_line_edit.setFont(QFont("Arial", 10))
            entry_name_line_edit.returnPressed.connect(lambda: [update_game_statistics_table('player_name', entry_name_line_edit.text()), self.player_name.setText(entry_name_line_edit.text())])
            entry_name_menu_list = [
                (entry_name_line_edit, lambda: None),
                (QPushButton("Ok"), lambda: [update_game_statistics_table('player_name', entry_name_line_edit.text()), self.player_name.setText(entry_name_line_edit.text())]),
                (QPushButton(""), lambda: None),
                (QPushButton(""), lambda: None),
                (QPushButton(""), lambda: None),
                (QPushButton(""), lambda: None),
                (QPushButton("<- Back to Menu", self), self.main_menu_zone)
            ]
            self.menu_zone(entry_name_menu_list)
        
        def ships_value():
            entry_ships = get_value_from_game_statistics('all_ships')
            entry_ships_spin_box = QSpinBox()
            entry_ships_spin_box.setMinimum(1)
            entry_ships_spin_box.setMaximum(10)
            entry_ships_spin_box.setValue(entry_ships)
            entry_ships_spin_box.setAlignment(Qt.AlignmentFlag.AlignCenter)
            entry_ships_spin_box.setFixedSize(130, 30)
            entry_ships_spin_box.setFont(QFont("Arial", 10))
            entry_ships_menu_list = [
                (QPushButton(""), lambda: None),
                (entry_ships_spin_box, lambda: None),
                (QPushButton("Ok"), lambda: update_game_statistics_table('all_ships', entry_ships_spin_box.value())),
                (QPushButton(""), lambda: None),
                (QPushButton(""), lambda: None),
                (QPushButton(""), lambda: None),
                (QPushButton("<- Back to Menu", self), self.main_menu_zone)
            ]
            self.menu_zone(entry_ships_menu_list)
        
        def level_value():
            entry_level = get_value_from_game_statistics('level')
            entry_level_menu_list = [
                (QPushButton(""), lambda: None),
                (QPushButton("Easy"), lambda: update_game_statistics_table('level', 'Easy')),
                (QPushButton("Normal"), lambda: update_game_statistics_table('level', 'Normal')),
                (QPushButton("Hard"), lambda: update_game_statistics_table('level', 'Hard')),
                (QPushButton(""), lambda: None),
                (QPushButton(""), lambda: None),
                (QPushButton("<- Back to Menu", self), self.main_menu_zone)
            ]
            self.menu_zone(entry_level_menu_list)
        
        self.setup_menu_list = [
            (QPushButton("Player Name", self), player_name_value),
            (QPushButton("Ships", self), ships_value),
            (QPushButton("Level", self), level_value),
            (QPushButton(""), lambda: None),
            (QPushButton(""), lambda: None),
            (QPushButton(""), lambda: None),
            (QPushButton("<- Back to Menu", self), self.main_menu_zone)
        ]
        self.menu_zone(self.setup_menu_list)
    
    def reset_game(self):
        '''Method responsible for restoring game settings to the starting settings, without having to restart the application.'''
        self.player_board = self.sea_zone(self.player_board_layout)
        self.cpu_board = self.sea_zone(self.cpu_board_layout)
        game_statistics_table_default()
        self.stat()
    
    def resizeEvent(self, event):
        size_window = event.size()
        self.width = size_window.width()
        self.height = size_window.height()
        # print(self.width, self.height)
        
        # update size QGraphicsView when change window size
        # self.view.setSceneRect(self.view.rect())


# opening file with style sheets
with open('data/styles/styles.css', "r") as file:
    style_sheet = file.read()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()    
    app.setStyleSheet(style_sheet)
    window.show()
    # window.showMaximized()
    sys.exit(app.exec())
