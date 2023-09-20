import sys, os, random, itertools, re, typing, time
from math import ceil

from data.db.db import (
    create_db,
    game_statistics_table_default,
    update_game_statistics_table,
    calculate_value_from_game_statistic,
    get_value_from_game_statistics,
    update_zones,
    get_zones,
    make_new_boards_table,
    update_boards_table,
    get_zone_from_boards,
    get_board_from_boards,
    checking_zone_brom_board,
    save_game_table_default,
    request_all_values_from_game_statistics_and_boards,
    save_file,
    load_file,
    read_files_list,
    delete_file,
    high_scores_table_default,
    add_high_scores,
    labels,
    read_high_scores,
    reset_high_scores,
)
from data.app.layouts import *
from data.sounds.sounds import *

from PyQt6.QtWidgets import (
    QMainWindow,
    QApplication,
    QWidget,
    QVBoxLayout,
    QGridLayout,
    QLabel,
    QGraphicsScene,
    QGraphicsView,
    QPushButton,
    QSizePolicy,
    QHBoxLayout,
    QMenuBar,
    QMenu,
    QSpinBox,
    QLineEdit,
    QStackedWidget,
    QStackedLayout,
    QInputDialog,
    QMessageBox,
    QTableWidget,
    QTableWidgetItem,
    QLayout,
    QBoxLayout,
    QGroupBox,
    QStyle,
    QTextEdit,
    QFileDialog,
    QSpacerItem,
    QCheckBox,
    QSlider,
    QRadioButton,
    QScrollBar,
)
from PyQt6.QtGui import (
    QPixmap,
    QIcon,
    QImage,
    QBrush,
    QFont,
    QPainter,
    QAction,
    QCursor,
    QPalette,
    QColor,
    QTextCursor,
    QGuiApplication,
)
from PyQt6.QtCore import (
    QSize,
    Qt,
    QRectF,
    QTimer,
    QFileInfo,
    QBuffer,
    QCoreApplication,
    QUrlQuery,
    QRect,
    QThread,
    QSettings,
)
from PyQt6.QtSql import QSqlDatabase, QSqlQuery
from PyQt6 import QtCore, QtGui
from PyQt6.QtCore import QUrl, QMargins, Qt
from PyQt6.QtMultimedia import QSoundEffect, QMediaPlayer, QAudioOutput


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # making datebase
        create_db()
        # making new tables, default
        game_statistics_table_default()
        high_scores_table_default()
        save_game_table_default()
        make_new_boards_table()

        self.initUI()

    def initUI(self):
        # main window settings
        self.setWindowTitle("Battle Ships v3.0")
        self.setWindowIcon(QIcon(r"data/images/main/fav.png"))

        # MENUBAR
        self.menu_bar = QMenuBar(self)  # making menu bar
        self.menu_bar.setObjectName("menu_bar")
        self.setMenuBar(self.menu_bar)
        self.menu_game = QMenu("Game", self.menu_bar)  # making menu
        self.menu_game.setObjectName("menu_game")
        self.menu_help = QMenu("Help", self.menu_bar)
        self.menu_help.setObjectName("menu_help")
        self.menu_bar.addMenu(self.menu_game)
        self.menu_bar.addMenu(self.menu_help)
        self.action_load_game = QAction("Load Game", self)
        self.action_load_game.setObjectName("load_game")
        self.action_load_game.setIcon(QIcon(r"data/images/main/load.png"))
        self.action_load_game.triggered.connect(self.load_game_layout)
        self.action_save_game = QAction("Save Game", self)
        self.action_save_game.setObjectName("save_game")
        self.action_save_game.setIcon(QIcon(r"data/images/main/save.PNG"))
        self.action_save_game.triggered.connect(self.save_game_layout)
        self.action_save_game.setEnabled(False)
        self.action_settings = QAction("Settings", self)
        self.action_settings.setObjectName("settings")
        self.action_settings.setIcon(QIcon(r"data\images\main\settings.png"))
        self.action_settings.triggered.connect(self.settings_layout)
        self.action_high_scores = QAction("High Scores", self)
        self.action_high_scores.setObjectName("high_scores")
        self.action_high_scores.setIcon(QIcon(r"data/images/main/top10.png"))
        # self.action_high_scores.triggered.connect(lambda: [self.fill_out_highscore_table(), self.highscores_layout()])
        self.action_high_scores.triggered.connect(lambda: self.highscores_layout())
        self.action_exit = QAction("Exit", self)  # making element of action
        self.action_exit.setObjectName("action_exit")
        self.action_exit.setIcon(QIcon(r"data/images/main/exit.png"))
        self.action_exit.triggered.connect(self.close)
        self.action_rules = QAction("Rules", self)
        self.action_rules.setIcon(QIcon(r"data/images/main/rules.png"))
        self.action_rules.triggered.connect(self.rules_layout)
        self.action_about = QAction("About", self)  # making action
        self.action_about.setIcon(QIcon(r"data/images/main/fav.png"))
        self.action_about.triggered.connect(self.about_layout)

        # adding action of element to menu
        self.menu_game.addAction(self.action_load_game)
        self.menu_game.addAction(self.action_save_game)
        self.menu_game.addAction(self.action_settings)
        self.menu_game.addAction(self.action_high_scores)
        self.menu_game.addSeparator()
        self.menu_game.addAction(self.action_exit)
        self.menu_help.addAction(self.action_rules)
        self.menu_help.addAction(self.action_about)

        # CENTRAL widget
        self.central_widget = QWidget()
        self.central_widget.setObjectName("central_widget")

        # tworzenie QStackedLayout
        self.stacked_layout = QStackedLayout(self.central_widget)
        # self.stacked_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setMinimumSize(1000, 750)

        # tworzenie głównego widgeta
        self.main_widget = QWidget()
        self.main_widget.setMaximumSize(200, 300)
        self.main_layout = QVBoxLayout()
        self.main_menu_buttons_list = [
            QPushButton("Start Battle", clicked=lambda: self.start_battle_layout()),
            QPushButton("Player Fleet", clicked=lambda: self.player_fleet_layout()),
            QPushButton(
                "Random Fleets",
                clicked=lambda: [self.random_fleet("player"), self.random_fleet("cpu")],
            ),
            QPushButton("Setup Game", clicked=self.setup_game_layout),
            QPushButton("Reset Game", clicked=self.reset_game),
            QPushButton("Quit Game", clicked=self.close),
        ]
        for btn in self.main_menu_buttons_list:
            self.buttons(btn)
            self.main_layout.addWidget(
                btn,
                0,
                QtCore.Qt.AlignmentFlag.AlignHCenter
                | QtCore.Qt.AlignmentFlag.AlignVCenter,
            )
        self.main_info = QLabel("Battle Ships v3.0 2023\u00AE")
        self.main_layout.addWidget(
            self.main_info,
            0,
            QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignVCenter,
        )
        self.main_widget.setLayout(self.main_layout)

        self.a = QWidget()
        main_layout = QHBoxLayout(self.a)
        main_layout.addWidget(self.main_widget)
        # dodawanie głównego widgeta do QStackedLayout
        self.stacked_layout.addWidget(self.a)

        # ustawianie QStackedLayout jako główny layout okna
        self.setCentralWidget(self.central_widget)
        # self.centralWidget().setLayout(self.stacked_layout)
        self.centralWidget().setContentsMargins(50, 25, 50, 25)

    # LAYOUTS methods
    def main_menu_layout(self):
        sea_sound.sea_sound_stop()
        self.action_save_game.setEnabled(False)
        self.action_load_game.setEnabled(True)
        if get_value_from_game_statistics("turns") != 0:
            self.main_menu_buttons_list[0].setText("Continue Battle")
            self.main_menu_buttons_list[1].setEnabled(False)
            self.main_menu_buttons_list[2].setEnabled(False)
            self.main_menu_buttons_list[3].setEnabled(False)
        self.stacked_layout.setCurrentWidget(self.a)

    def start_battle_layout(self):
        # Check the completeness of both fleets.

        if get_value_from_game_statistics("turns") == 0:
            if get_value_from_game_statistics("player_ships") != self.level_game(
                "player"
            ):
                self.main_info.setText("Fleets not complete.")
                return
            self.random_fleet("cpu")
            self.action_save_game.setEnabled(True)
            self.action_load_game.setEnabled(False)
            self.music_and_sounds("sound", "sea_start")
        elif get_value_from_game_statistics("turns") != 0:
            self.action_save_game.setEnabled(True)
            self.action_load_game.setEnabled(False)
            self.music_and_sounds("sound", "sea_start")

        # PLAYER widget
        player_widget = QWidget(self.central_widget)
        player_widget.setObjectName("player_widget")
        player_widget.setMaximumSize(350, 600)

        self.widget = QWidget(player_widget)
        player_widget_layout = QVBoxLayout(self.widget)

        # name
        player_name = QLabel(get_value_from_game_statistics("player_name"), self.widget)
        player_name.setObjectName("name")
        # player_name.setContentsMargins(20, 5, 10, 5)
        # player_name.setFont(QFont("Arial", 12))
        player_widget_layout.addWidget(
            player_name,
            0,
            QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignVCenter,
        )

        # board
        player_board_layout = QGridLayout()
        player_board_layout.setSpacing(0)
        self.player_board = self.sea_zone("player", player_board_layout)

        # stats
        player_statistics_layout = QVBoxLayout()
        player_statistics_layout.setContentsMargins(10, 5, 10, 5)
        self.player_info = QLabel("Info", player_widget)
        self.player_statistic_1 = QLabel("Ships", player_widget)
        self.player_statistic_2 = QLabel("Avaiable Shots", player_widget)
        self.player_statistic_3 = QLabel("Shots (All)", player_widget)
        self.player_statistic_4 = QLabel("Hit shots", player_widget)
        self.player_statistic_5 = QLabel("Missed shots", player_widget)
        self.player_statistic_6 = QLabel("Effective", player_widget)
        player_statistics_layout.addWidget(
            self.player_info,
            0,
            QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignVCenter,
        )
        player_statistics_layout.addWidget(self.player_statistic_1)
        player_statistics_layout.addWidget(self.player_statistic_2)
        player_statistics_layout.addWidget(self.player_statistic_3)
        player_statistics_layout.addWidget(self.player_statistic_4)
        player_statistics_layout.addWidget(self.player_statistic_5)
        player_statistics_layout.addWidget(self.player_statistic_6)

        player_widget_layout.addLayout(player_board_layout)
        player_widget_layout.addLayout(player_statistics_layout)

        player_widget.setLayout(player_widget_layout)

        # CPU widget
        cpu_widget = QWidget(self.central_widget)
        cpu_widget.setObjectName("cpu_widget")
        cpu_widget.setMaximumSize(350, 600)

        self.widget = QWidget(cpu_widget)
        cpu_widget_layout = QVBoxLayout(self.widget)

        # name
        cpu_name = QLabel("CPU", self.widget)
        cpu_name.setObjectName("name")
        cpu_widget_layout.addWidget(
            cpu_name,
            0,
            QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignVCenter,
        )

        # board
        cpu_board_layout = QGridLayout()
        cpu_board_layout.setSpacing(0)
        self.cpu_board = self.sea_zone("cpu", cpu_board_layout)
        for i in range(0, 100):
            try:
                self.cpu_board[i].disconnect()
            except TypeError:
                pass
            self.cpu_board[i].clicked.connect(
                lambda checked, button=self.cpu_board[i]: [
                    self.shot("player", self.cpu_board.index(button), button, True)
                ]
            )

        # stats
        cpu_statistics_layout = QVBoxLayout()
        cpu_statistics_layout.setContentsMargins(10, 5, 10, 5)
        self.cpu_info = QLabel("Info", cpu_widget)
        self.cpu_statistic_1 = QLabel("Ships", cpu_widget)
        self.cpu_statistic_2 = QLabel("Avaiable Shots", cpu_widget)
        self.cpu_statistic_3 = QLabel("Shots (All)", cpu_widget)
        self.cpu_statistic_4 = QLabel("Hit shots", cpu_widget)
        self.cpu_statistic_5 = QLabel("Missed shots", cpu_widget)
        self.cpu_statistic_6 = QLabel("Effective", cpu_widget)
        cpu_statistics_layout.addWidget(
            self.cpu_info,
            0,
            QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignVCenter,
        )
        cpu_statistics_layout.addWidget(self.cpu_statistic_1)
        cpu_statistics_layout.addWidget(self.cpu_statistic_2)
        cpu_statistics_layout.addWidget(self.cpu_statistic_3)
        cpu_statistics_layout.addWidget(self.cpu_statistic_4)
        cpu_statistics_layout.addWidget(self.cpu_statistic_5)
        cpu_statistics_layout.addWidget(self.cpu_statistic_6)

        cpu_widget_layout.addLayout(cpu_board_layout)
        cpu_widget_layout.addLayout(cpu_statistics_layout)

        cpu_widget.setLayout(cpu_widget_layout)

        # NAV
        nav_widget = QWidget(self.central_widget)
        nav_widget.setMaximumSize(200, 300)
        widget = QWidget(nav_widget)
        nav_layout = QVBoxLayout(widget)
        retreat_button = QPushButton("Retreat", clicked=lambda: print("wycoduję się"))
        back_to_menu = QPushButton("<- Back to Menu", clicked=self.main_menu_layout)
        self.buttons(retreat_button)
        self.buttons(back_to_menu)
        spacer = QSpacerItem(
            20, 400, QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Expanding
        )
        nav_layout.addItem(spacer)
        nav_layout.addWidget(
            retreat_button,
            1,
            Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignBottom,
        )
        nav_layout.addWidget(
            back_to_menu,
            0,
            Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignBottom,
        )
        nav_widget.setLayout(nav_layout)
        nav_layout.setSpacing(0)

        b = QWidget()
        main_layout = QHBoxLayout(b)
        main_layout.addWidget(player_widget)
        main_layout.addWidget(cpu_widget)
        main_layout.addWidget(nav_widget)

        self.stat()
        # dodawanie widgeta do QStackedLayout
        self.stacked_layout.addWidget(b)
        # ustawianie drugiego widgeta jako aktualny widget QStackedLayout
        self.stacked_layout.setCurrentWidget(b)

        self.start_time_game = time.time()

        # who start battle?
        if get_value_from_game_statistics("turns") == 0:
            sides = [self.player_turn, self.cpu_turn]
            start = random.choice(sides)
            start()
        else:
            self.player_turn()

    def player_fleet_layout(self):
        if get_value_from_game_statistics("turns") != 0:
            self.main_info.setText("You cannot change your fleet \n during the battle!")
            return

        def enabled_check():
            if get_value_from_game_statistics("player_ships") == self.level_game(
                "player"
            ):
                self.ready_to_battle.setEnabled(True)
            else:
                self.ready_to_battle.setEnabled(False)
            if get_value_from_game_statistics("player_ships") != 0:
                self.clear_board.setEnabled(True)
            else:
                self.clear_board.setEnabled(False)

        # PLAYER widget
        player_widget = QWidget(self.central_widget)
        player_widget.setObjectName("player_widget")
        player_widget.setMaximumSize(350, 600)

        self.widget = QWidget(player_widget)

        player_widget_layout = QVBoxLayout(self.widget)

        # name
        player_name = QLabel(get_value_from_game_statistics("player_name"), self.widget)
        player_name.setContentsMargins(20, 5, 10, 5)
        player_name.setFont(QFont("Arial", 12))
        player_widget_layout.addWidget(
            player_name,
            0,
            QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignVCenter,
        )

        # board
        player_board_layout = QGridLayout()
        player_board_layout.setSpacing(0)

        # ships
        amount_ships = QLabel(
            f"Ships: {get_value_from_game_statistics('player_ships')}", player_widget
        )
        amount_ships.setObjectName("player_statistic_1")
        max_ships = QLabel(f"Max. Ships: {self.level_game('player')}")
        player_board = self.sea_zone("player", player_board_layout)
        for i in range(0, len(player_board)):
            # player_board[i].setEnabled(True)
            try:
                player_board[i].disconnect()
            except TypeError:
                pass
            player_board[i].clicked.connect(
                lambda zone=player_board[i], index=i, amount=4: [
                    self.ship("player", index, True, amount),
                    amount_ships.setText(
                        f"Ships: {get_value_from_game_statistics('player_ships')}"
                    ),
                    enabled_check(),
                ]
            )

        # NAV
        nav_widget = QWidget(self.central_widget)
        nav_widget.setMaximumSize(200, 300)
        widget = QWidget(nav_widget)
        nav_layout = QVBoxLayout(widget)
        self.ready_to_battle = QPushButton(
            "Ready to Battle!", clicked=lambda: self.start_battle_layout()
        )
        self.ready_to_battle.setEnabled(False)
        self.clear_board = QPushButton(
            "Clear Player Board",
            clicked=lambda: [
                self.clear_player_board(),
                amount_ships.setText(
                    f"Ships: {get_value_from_game_statistics('player_ships')}"
                ),
            ],
        )
        self.clear_board.setEnabled(False)
        back_button = QPushButton("<- Back to Menu", clicked=self.main_menu_layout)
        self.buttons(self.ready_to_battle)
        self.buttons(self.clear_board)
        self.buttons(back_button)
        spacer = QSpacerItem(
            20, 400, QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Expanding
        )
        nav_layout.addItem(spacer)
        enabled_check()
        nav_layout.addWidget(self.ready_to_battle)
        nav_layout.addWidget(self.clear_board)
        nav_layout.addWidget(back_button)
        nav_widget.setLayout(nav_layout)
        nav_layout.setSpacing(0)

        # dodawanie layoutów i widgetów do player_fleet_layout
        player_widget_layout.addLayout(player_board_layout)
        player_widget_layout.addWidget(amount_ships)
        player_widget_layout.addWidget(max_ships)
        player_widget_layout.addWidget(QWidget())
        player_widget.setLayout(player_widget_layout)

        c = QWidget()
        main_layout = QHBoxLayout(c)
        main_layout.addWidget(player_widget)
        main_layout.addWidget(nav_widget)

        # dodawanie drugiego widgeta do QStackedLayout
        self.stacked_layout.addWidget(c)
        # ustawianie drugiego widgeta jako aktualny widget QStackedLayout
        self.stacked_layout.setCurrentWidget(c)

    def setup_game_layout(self):
        def replace_button(button):
            if button.text() == "Player Name":
                new_line = QLineEdit(button.setText(""), button.parent())
                new_line.setGeometry(button.geometry())
                new_line.setPlaceholderText("Your Name...")
                new_line.setMaxLength(10)
                new_line.setAlignment(Qt.AlignmentFlag.AlignCenter)
                new_line.setFocus()
                new_line.setMaxLength(16)
                new_line.setFixedSize(130, 30)
                new_line.setFont(QFont("Arial", 10))
                new_line.returnPressed.connect(
                    lambda: update_game_statistics_table("player_name", new_line.text())
                )
                new_line.show()
                main_menu_buttons_list[1].setText("Ok")
                main_menu_buttons_list[1].disconnect()
                main_menu_buttons_list[1].clicked.connect(
                    lambda: update_game_statistics_table("player_name", new_line.text())
                )
                main_menu_buttons_list[2].setText("")
                main_menu_buttons_list[4].setText("<- Back to Setup")
                main_menu_buttons_list[4].disconnect()
                main_menu_buttons_list[4].clicked.connect(self.setup_game_layout)

            if button.text() == "Max. Ships":
                entry_ships = get_value_from_game_statistics("all_ships")
                new_line = QSpinBox(button.parent())
                new_line.setGeometry(button.geometry())
                new_line.setMinimum(1)
                new_line.setMaximum(10)
                new_line.setValue(entry_ships)
                new_line.setAlignment(Qt.AlignmentFlag.AlignCenter)
                new_line.setFixedSize(130, 30)
                new_line.setFont(QFont("Arial", 10))
                new_line.show()
                main_menu_buttons_list[0].setText("")
                main_menu_buttons_list[0].disconnect()
                main_menu_buttons_list[2].setText("Ok")
                main_menu_buttons_list[2].disconnect()
                main_menu_buttons_list[2].clicked.connect(
                    lambda: update_game_statistics_table("all_ships", new_line.value())
                )
                main_menu_buttons_list[4].setText("<- Back to Setup")
                main_menu_buttons_list[4].disconnect()
                main_menu_buttons_list[4].clicked.connect(self.setup_game_layout)

            if button.text() == "Level":
                main_menu_buttons_list[0].setText("")
                main_menu_buttons_list[0].disconnect()
                main_menu_buttons_list[1].setText("Easy")
                main_menu_buttons_list[1].disconnect()
                main_menu_buttons_list[1].clicked.connect(
                    lambda: update_game_statistics_table("level", "Easy")
                )
                main_menu_buttons_list[2].setText("Normal")
                main_menu_buttons_list[2].disconnect()
                main_menu_buttons_list[2].clicked.connect(
                    lambda: update_game_statistics_table("level", "Normal")
                )
                main_menu_buttons_list[3].setEnabled(True)
                main_menu_buttons_list[3].setText("Hard")
                main_menu_buttons_list[3].disconnect()
                main_menu_buttons_list[3].clicked.connect(
                    lambda: update_game_statistics_table("level", "Hard")
                )
                main_menu_buttons_list[4].setText("<- Back to Setup")
                main_menu_buttons_list[4].disconnect()
                main_menu_buttons_list[4].clicked.connect(self.setup_game_layout)

        # tworzenie głównego widgeta
        self.main_widget = QWidget()
        self.main_widget.setMaximumSize(200, 300)
        self.main_layout = QVBoxLayout()
        main_menu_buttons_list = [
            QPushButton(
                "Player Name", clicked=lambda: replace_button(main_menu_buttons_list[0])
            ),
            QPushButton(
                "Max. Ships", clicked=lambda: replace_button(main_menu_buttons_list[1])
            ),
            QPushButton(
                "Level", clicked=lambda: replace_button(main_menu_buttons_list[2])
            ),
            QPushButton("", clicked=lambda: None),
            QPushButton("<- Back to Menu", clicked=self.main_menu_layout),
        ]
        for btn in main_menu_buttons_list:
            self.buttons(btn)
            self.main_layout.addWidget(
                btn,
                0,
                QtCore.Qt.AlignmentFlag.AlignHCenter
                | QtCore.Qt.AlignmentFlag.AlignVCenter,
            )
        self.main_info = QLabel("Battle Ships v3.0 2023\u00AE")
        self.main_layout.addWidget(
            self.main_info,
            0,
            QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignVCenter,
        )
        self.main_widget.setLayout(self.main_layout)

        self.d = QWidget()
        main_layout = QHBoxLayout(self.d)
        main_layout.addWidget(self.main_widget)

        # dodawanie głównego widgeta do QStackedLayout
        self.stacked_layout.addWidget(self.d)
        self.stacked_layout.setCurrentWidget(self.d)

    def about_layout(self):
        # ABOUT widget
        about_widget = QWidget(self.central_widget)
        about_widget.setObjectName("about_widget")
        about_widget.setMaximumSize(350, 600)

        self.widget = QWidget(about_widget)

        about_widget_layout = QVBoxLayout(about_widget)
        about_widget_layout.addWidget(QWidget())
        # title
        title_game = QLabel("Battle Ships v3.0", self.widget)
        title_game.setContentsMargins(20, 5, 10, 5)
        title_game.setFont(QFont("Arial", 12))
        about_widget_layout.addWidget(
            title_game,
            0,
            QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignVCenter,
        )

        # date
        date_completed = QLabel("April 19th, 2023", self.widget)
        date_completed.setContentsMargins(20, 5, 10, 5)
        date_completed.setFont(QFont("Arial", 12))
        about_widget_layout.addWidget(
            date_completed,
            0,
            QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignVCenter,
        )

        # author
        author = QLabel("Lukasz Szabat", self.widget)
        author.setContentsMargins(20, 5, 10, 5)
        author.setFont(QFont("Arial", 12))
        about_widget_layout.addWidget(
            author,
            0,
            QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignVCenter,
        )

        # contact
        email = "<a href='mailto:synvoret@gmail.com'>synvoret@gmail.com</a>"
        contact = QLabel("", self.widget)
        contact.setObjectName("contact")
        contact.setText(email)
        contact.setOpenExternalLinks(True)
        contact.setContentsMargins(20, 5, 10, 5)
        font = QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setUnderline(False)
        contact.setFont(font)
        about_widget_layout.addWidget(
            contact,
            0,
            QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignVCenter,
        )
        about_widget_layout.addWidget(QWidget())

        # nav
        nav_widget = QWidget(self.central_widget)
        nav_widget.setMaximumSize(200, 300)
        widget = QWidget(nav_widget)
        nav_layout = QVBoxLayout(widget)
        back_game_button = QPushButton(
            "<- Back to Game", clicked=self.start_battle_layout
        )
        if get_value_from_game_statistics("player_ships") == 0:
            back_game_button.setEnabled(False)
        back_menu_button = QPushButton("<- Back to Menu", clicked=self.main_menu_layout)
        self.buttons(back_menu_button)
        self.buttons(back_game_button)
        spacer = QSpacerItem(
            20, 400, QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Expanding
        )
        nav_layout.addItem(spacer)
        nav_layout.addWidget(back_game_button)
        nav_layout.addWidget(back_menu_button)
        nav_widget.setLayout(nav_layout)
        nav_layout.setSpacing(0)

        e = QWidget()
        main_layout = QHBoxLayout(e)
        main_layout.addWidget(about_widget)
        main_layout.addWidget(nav_widget)
        # dodawanie głównego widgeta do QStackedLayout
        self.stacked_layout.addWidget(e)
        self.stacked_layout.setCurrentWidget(e)

    def rules_layout(self):
        # RULES widget
        rules_widget = QWidget(self.central_widget)
        rules_widget.setObjectName("about_widget")
        rules_widget.setMaximumSize(350, 600)

        self.widget = QWidget(rules_widget)

        rules_widget_layout = QVBoxLayout(rules_widget)
        rules_widget_layout.addWidget(QWidget())

        # title game
        title_game = QLabel("Battle Ships v3.0", self.widget)
        title_game.setContentsMargins(20, 5, 10, 5)
        title_game.setFont(QFont("Arial", 12))
        rules_widget_layout.addWidget(
            title_game,
            0,
            QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignVCenter,
        )

        # title
        title = QLabel("Rules", self.widget)
        title.setContentsMargins(20, 5, 10, 5)
        title.setFont(QFont("Arial", 12))
        rules_widget_layout.addWidget(
            title,
            0,
            QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignVCenter,
        )

        # amount ships
        amount_ships = QLabel("Amount Ships (default): 4", self.widget)
        amount_ships.setContentsMargins(20, 5, 10, 5)
        amount_ships.setFont(QFont("Arial", 12))
        rules_widget_layout.addWidget(
            amount_ships,
            0,
            QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignVCenter,
        )

        # max. ships
        max_ships = QLabel("Max. Ships: 10", self.widget)
        max_ships.setContentsMargins(20, 5, 10, 5)
        max_ships.setFont(QFont("Arial", 12))
        rules_widget_layout.addWidget(
            max_ships,
            0,
            QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignVCenter,
        )

        # level
        level = QLabel("Level (default): Normal", self.widget)
        level.setContentsMargins(20, 5, 10, 5)
        level.setFont(QFont("Arial", 12))
        rules_widget_layout.addWidget(
            level,
            0,
            QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignVCenter,
        )

        # difficulty levels
        difficulty_levels = QLabel("Difficulty Levels: Easy, Normal, Hard", self.widget)
        difficulty_levels.setContentsMargins(20, 5, 10, 5)
        difficulty_levels.setFont(QFont("Arial", 12))
        rules_widget_layout.addWidget(
            difficulty_levels,
            0,
            QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignVCenter,
        )

        # level rules
        level_rules1 = QLabel("Level Rules - Easy: Player +1 ship", self.widget)
        level_rules1.setContentsMargins(20, 5, 10, 5)
        level_rules1.setFont(QFont("Arial", 12))
        rules_widget_layout.addWidget(
            level_rules1,
            0,
            QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignVCenter,
        )

        # level rules
        level_rules2 = QLabel("Level Rules - Hard: CPU +1 ship", self.widget)
        level_rules2.setContentsMargins(20, 5, 10, 5)
        level_rules2.setFont(QFont("Arial", 12))
        rules_widget_layout.addWidget(
            level_rules2,
            0,
            QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignVCenter,
        )

        # available shots
        available_shots = QLabel("Available Shots: Active Ships / 2", self.widget)
        available_shots.setContentsMargins(20, 5, 10, 5)
        available_shots.setFont(QFont("Arial", 12))
        rules_widget_layout.addWidget(
            available_shots,
            0,
            QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignVCenter,
        )

        # ship by ship
        ship_by_ship = QLabel("Ship by Ship: No", self.widget)
        ship_by_ship.setContentsMargins(20, 5, 10, 5)
        ship_by_ship.setFont(QFont("Arial", 12))
        rules_widget_layout.addWidget(
            ship_by_ship,
            0,
            QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignVCenter,
        )
        rules_widget_layout.addWidget(QWidget())

        # nav
        nav_widget = QWidget(self.central_widget)
        nav_widget.setMaximumSize(200, 300)
        widget = QWidget(nav_widget)
        nav_layout = QVBoxLayout(widget)
        back_game_button = QPushButton(
            "<- Back to Game", clicked=self.start_battle_layout
        )
        if get_value_from_game_statistics("player_ships") == 0:
            back_game_button.setEnabled(False)
        back_menu_button = QPushButton("<- Back to Menu", clicked=self.main_menu_layout)
        self.buttons(back_game_button)
        self.buttons(back_menu_button)
        spacer = QSpacerItem(
            20, 400, QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Expanding
        )
        nav_layout.addItem(spacer)
        nav_layout.addWidget(back_game_button)
        nav_layout.addWidget(back_menu_button)
        nav_widget.setLayout(nav_layout)
        nav_layout.setSpacing(0)

        f = QWidget()
        main_layout = QHBoxLayout(f)
        main_layout.addWidget(rules_widget)
        main_layout.addWidget(nav_widget)
        # dodawanie głównego widgeta do QStackedLayout
        self.stacked_layout.addWidget(f)
        self.stacked_layout.setCurrentWidget(f)

    def load_game_layout(self):
        # saves
        loads = read_files_list()
        save_positions = [QPushButton(load[0]) for load in loads]
        load_image = QPixmap("data\images\main\load.png").scaled(QSize(30, 30))
        load_icon = QIcon(load_image)

        def set_icon(button, buttons=save_positions):
            try:
                if (
                    button.icon().pixmap(button.icon().availableSizes()[0]).toImage()
                    == load_image.toImage()
                ):
                    button.setIcon(QIcon())
            except:
                button.setIcon(load_icon)
            for btn in buttons:
                if btn != button and btn.icon():
                    btn.setIcon(QIcon())

        def load_with_icon(buttons=save_positions):
            def load_game(name):
                loaded_data: dict = load_file(name)
                for data in loaded_data["gs"].items():
                    update_game_statistics_table(data[0], data[1])
                for data in loaded_data["b"].items():
                    update_boards_table("player", data[1][0], data[0])
                    update_boards_table("cpu", data[1][1], data[0])

            for but in save_positions:
                try:
                    if (
                        but.icon().pixmap(but.icon().availableSizes()[0]).toImage()
                        == load_image.toImage()
                    ):
                        load_game(but.text())
                except IndexError:
                    pass

            self.start_battle_layout()

        def delete_save(buttons=save_positions):
            for but in buttons:
                try:
                    if (
                        but.icon().pixmap(but.icon().availableSizes()[0]).toImage()
                        == load_image.toImage()
                    ):
                        delete_file(but.text())
                except IndexError:
                    pass

        # LOAD widget
        load_widget = QWidget(self.central_widget)
        load_widget.setObjectName("load_widget")
        load_widget.setMaximumSize(350, 600)

        self.widget = QWidget(load_widget)

        load_widget_layout = QVBoxLayout(load_widget)

        for i in range(0, len(save_positions)):
            line = QHBoxLayout()
            pos = save_positions[i]
            pos.clicked.connect(lambda _, b=pos: set_icon(b))
            pos.setObjectName("pos")
            pos.setFont(QFont("Arial", 12))
            pos.setMaximumSize(300, 30)
            line.addWidget(pos, i, Qt.AlignmentFlag.AlignTop)
            load_widget_layout.addLayout(line)
        spacerItem = QSpacerItem(
            20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding
        )
        load_widget_layout.addItem(spacerItem)

        # nav
        nav_widget = QWidget(self.central_widget)
        nav_widget.setMaximumSize(200, 300)
        widget = QWidget(nav_widget)
        nav_layout = QVBoxLayout(widget)
        load_button = QPushButton("Load Game", clicked=load_with_icon)
        delete_button = QPushButton(
            "Dalete Save",
            clicked=lambda: [
                self.delete_accept(
                    delete_save,
                    "DELETE save?!",
                    "Are you sure You want to DELETE save?? ",
                ),
                self.load_game_layout(),
            ],
        )
        back_button = QPushButton("<- Back to Menu", clicked=self.main_menu_layout)
        self.buttons(load_button)
        self.buttons(delete_button)
        self.buttons(back_button)
        spacer = QSpacerItem(
            20, 400, QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Expanding
        )
        nav_layout.addItem(spacer)
        nav_layout.addWidget(load_button)
        nav_layout.addWidget(delete_button)
        nav_layout.addWidget(back_button)
        nav_widget.setLayout(nav_layout)
        nav_layout.setSpacing(0)

        g = QWidget()
        main_layout = QHBoxLayout(g)
        main_layout.addWidget(load_widget)
        main_layout.addWidget(nav_widget)
        # dodawanie głównego widgeta do QStackedLayout
        self.stacked_layout.addWidget(g)
        self.stacked_layout.setCurrentWidget(g)

    def save_game_layout(self):
        loads = read_files_list()
        save_image = QPixmap("data\images\main\save.PNG").scaled(QSize(30, 30))
        save_icon = QIcon(save_image)
        d = {}

        def set_icon(button, buttons=d):
            if not button:
                for btn in buttons:
                    if isinstance(buttons[btn], QPushButton):
                        if buttons[btn] != button and buttons[btn].icon():
                            buttons[btn].setIcon(QIcon())
                return
            try:
                if (
                    button.icon().pixmap(button.icon().availableSizes()[0]).toImage()
                    == save_image.toImage()
                ):
                    button.setIcon(QIcon())
            except:
                button.setIcon(save_icon)
            for btn in buttons:
                if isinstance(buttons[btn], QPushButton):
                    if buttons[btn] != button and buttons[btn].icon():
                        buttons[btn].setIcon(QIcon())

        def save_with_icon(name):
            datas_to_save = request_all_values_from_game_statistics_and_boards("save")

            if len(read_files_list()) > 10:
                return

            save_name = name.text()
            # save_name = name.text()

            if len(save_name) == 0:
                return

            if save_file(save_name, datas_to_save) is not False:
                self.save_game_layout()
                # print('zapis stanu gry przebiegł pomyślnie')
            else:
                print("nie zapisałem bo taka nazwa istnieje w bazie danych")

        def delete_save(buttons=d):
            for btn in buttons:
                try:
                    if isinstance(buttons[btn], QPushButton):
                        if (
                            buttons[btn]
                            .icon()
                            .pixmap(buttons[btn].icon().availableSizes()[0])
                            .toImage()
                            == save_image.toImage()
                        ):
                            delete_file(buttons[btn].text())
                except IndexError:
                    pass

        # SAVE widget
        save_widget = QWidget(self.central_widget)
        save_widget.setObjectName("save_widget")
        save_widget.setMaximumSize(350, 600)

        self.widget = QWidget(save_widget)

        save_widget_layout = QVBoxLayout(save_widget)

        for i in range(len(loads)):
            if i < len(loads):
                d[i] = QPushButton(loads[i][0])

        d[len(loads)] = QLineEdit()

        for i in range(len(list(d.values()))):
            line = QHBoxLayout()
            widget = d[i]
            widget.setObjectName("pos")
            widget.setFont(QFont("Arial", 12))
            widget.setMaximumSize(300, 30)
            if isinstance(widget, QPushButton):
                widget_button = widget
                widget_button.setText(widget.text())
                widget_button.clicked.connect(lambda _, b=widget_button: set_icon(b))
            elif isinstance(widget, QLineEdit):
                widget_lineedit = widget
                widget_lineedit.clearFocus()
                widget_lineedit.setPlaceholderText("-- empty slot --")
                widget_lineedit.setAlignment(Qt.AlignmentFlag.AlignCenter)
                widget_lineedit.returnPressed.connect(
                    lambda text=widget_lineedit: save_with_icon(text)
                )
                widget_lineedit.installEventFilter(self)
                widget_lineedit.editingFinished.connect(lambda: print("mam tę linię"))
                widget_lineedit.cursorPositionChanged.connect(lambda: set_icon(False))
                # line.addWidget(widget_lineedit)
            line.addWidget(widget)
            save_widget_layout.addLayout(line)
        spacerItem = QSpacerItem(
            20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding
        )
        save_widget_layout.addItem(spacerItem)

        # nav
        nav_widget = QWidget(self.central_widget)
        nav_widget.setMaximumSize(200, 300)
        new_widget = QWidget(nav_widget)
        nav_layout = QVBoxLayout(widget)
        ########################## TODO (doesn't save game after click button 'save_button')
        # save_button = QPushButton('Save Game', clicked=lambda text=widget_lineedit.text(): save_with_icon(text))
        save_button = QPushButton(
            "Save Game", clicked=lambda: print(widget_lineedit.text())
        )
        ##########################
        delete_button = QPushButton(
            "Dalete Save",
            clicked=lambda: [
                self.delete_accept(
                    delete_save,
                    "DELETE save?!",
                    "Are you sure You want to DELETE save?? ",
                ),
                self.save_game_layout(),
            ],
        )
        back_button = QPushButton("<- Back to Game", clicked=self.start_battle_layout)
        self.buttons(save_button)
        self.buttons(delete_button)
        self.buttons(back_button)
        spacer = QSpacerItem(
            20, 400, QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Expanding
        )
        nav_layout.addItem(spacer)
        nav_layout.addWidget(save_button)
        nav_layout.addWidget(delete_button)
        nav_layout.addWidget(back_button)
        nav_widget.setLayout(nav_layout)
        nav_layout.setSpacing(0)

        h = QWidget()
        main_layout = QHBoxLayout(h)
        main_layout.addWidget(save_widget)
        main_layout.addWidget(nav_widget)
        self.stacked_layout.addWidget(h)
        self.stacked_layout.setCurrentWidget(h)

    def settings_layout(self):
        # SETTINGS widget
        settings_widget = QWidget(self.central_widget)
        settings_widget.setObjectName("settings_widget")
        settings_widget.setContentsMargins(40, 50, 40, 30)
        settings_widget.setMaximumSize(350, 600)

        self.widget = QWidget(settings_widget)

        settings_widget_layout = QVBoxLayout(settings_widget)

        # spacer = QSpacerItem(20, 400, QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Expanding)
        # settings_widget_layout.addItem(spacer)

        settings_label = QLabel("Settings")
        settings_label.setFont(QFont("Arial", 12))
        settings_widget_layout.addWidget(
            settings_label,
            0,
            Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignCenter,
        )

        # line = QHBoxLayout()
        # spacerItem = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        # line.addItem(spacerItem)
        # settings_widget_layout.addLayout(line)

        # player name
        line = QHBoxLayout()
        name = get_value_from_game_statistics("player_name")
        player_name = QLineEdit(name)
        player_name.setPlaceholderText("Your Name...")
        player_name.setMaxLength(10)
        player_name.setAlignment(Qt.AlignmentFlag.AlignCenter)
        player_name.setMaxLength(16)
        player_name.returnPressed.connect(
            lambda: update_game_statistics_table("player_name", player_name.text())
        )
        # player_name.setFixedSize(130, 30)
        mplayer_name_label = QLabel("Player Name")
        line.addWidget(
            player_name, 0, Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignCenter
        )
        line.addWidget(
            mplayer_name_label,
            0,
            Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignCenter,
        )
        settings_widget_layout.addLayout(line)

        # on/off sounds
        line = QHBoxLayout()
        sounds_fx = QCheckBox()
        sounds_fx.setChecked(bool(get_value_from_game_statistics("sounds")))
        sounds_fx_label = QLabel("Sounds")
        sounds_fx.stateChanged.connect(
            lambda: self.music_and_sounds(
                sound="sound", action="sea_stop", stan=int(sounds_fx.isChecked())
            )
        )
        line.addWidget(
            sounds_fx, 0, Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignCenter
        )
        line.addWidget(
            sounds_fx_label,
            0,
            Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignCenter,
        )
        settings_widget_layout.addLayout(line)

        # on/off music
        line = QHBoxLayout()
        music_fx = QCheckBox()
        music_fx.setChecked(bool(get_value_from_game_statistics("music")))
        music_fx_label = QLabel("Music")
        music_fx.stateChanged.connect(
            lambda: self.music_and_sounds("music", stan=int(music_fx.isChecked()))
        )
        line.addWidget(
            music_fx, 0, Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignCenter
        )
        line.addWidget(
            music_fx_label,
            0,
            Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignCenter,
        )
        settings_widget_layout.addLayout(line)

        # amount ships
        line = QHBoxLayout()
        actual_max_ships = get_value_from_game_statistics("all_ships")
        ships = QScrollBar(Qt.Orientation.Horizontal)
        # ships = QSlider(Qt.Orientation.Horizontal)
        ships.setFixedSize(130, 20)
        ships.setMinimum(1)
        ships.setMaximum(10)
        ships.setValue(actual_max_ships)
        ships.setSingleStep(1)
        ships_label = QLabel(f"Ships: {actual_max_ships}")
        ships.valueChanged.connect(
            lambda: [
                ships_label.setText("Ships: {}".format(ships.value())),
                update_game_statistics_table("all_ships", ships.value()),
            ]
        )
        line.addWidget(
            ships, 0, Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignCenter
        )
        line.addWidget(
            ships_label,
            0,
            QtCore.Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignCenter,
        )
        settings_widget_layout.addLayout(line)

        # level
        line = QHBoxLayout()
        levels = QVBoxLayout()
        level_e = QRadioButton("Easy")
        level_n = QRadioButton("Normal")
        level_h = QRadioButton("Hard")
        if get_value_from_game_statistics("level") == "Easy":
            level_e.setChecked(True)
        elif get_value_from_game_statistics("level") == "Normal":
            level_n.setChecked(True)
        elif get_value_from_game_statistics("level") == "Hard":
            level_h.setChecked(True)
        level_e.toggled.connect(
            lambda stan=level_e.isChecked(): update_game_statistics_table(
                "level", "Easy"
            )
            if stan
            else False
        )
        level_n.toggled.connect(
            lambda stan=level_n.isChecked(): update_game_statistics_table(
                "level", "Normal"
            )
            if stan
            else False
        )
        level_h.toggled.connect(
            lambda stan=level_h.isChecked(): update_game_statistics_table(
                "level", "Hard"
            )
            if stan
            else False
        )
        level_label = QLabel("Level")
        levels.addWidget(
            level_e, 0, Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignCenter
        )
        levels.addWidget(
            level_n, 0, Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignCenter
        )
        levels.addWidget(
            level_h, 0, Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignCenter
        )
        line.addLayout(levels)
        line.addWidget(
            level_label,
            0,
            QtCore.Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignCenter,
        )
        settings_widget_layout.addLayout(line)

        line = QHBoxLayout()
        spacerItem = QSpacerItem(
            20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding
        )
        line.addItem(spacerItem)
        settings_widget_layout.addLayout(line)

        # nav
        nav_widget = QWidget(self.central_widget)
        nav_widget.setMaximumSize(200, 300)
        widget = QWidget(nav_widget)
        nav_layout = QVBoxLayout(widget)
        back_game_button = QPushButton(
            "<- Back to Game", clicked=self.start_battle_layout
        )
        if get_value_from_game_statistics("player_ships") == 0:
            back_game_button.setEnabled(False)
        back_button = QPushButton("<- Back to Menu", clicked=self.main_menu_layout)
        self.buttons(back_game_button)
        self.buttons(back_button)
        spacer = QSpacerItem(
            20, 400, QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Expanding
        )
        nav_layout.addItem(spacer)
        nav_layout.addWidget(back_game_button)
        nav_layout.addWidget(back_button)
        nav_widget.setLayout(nav_layout)
        nav_layout.setSpacing(0)

        k = QWidget()
        main_layout = QHBoxLayout(k)
        main_layout.addWidget(settings_widget)
        main_layout.addWidget(nav_widget)
        # dodawanie głównego widgeta do QStackedLayout
        self.stacked_layout.addWidget(k)
        self.stacked_layout.setCurrentWidget(k)

    def highscores_layout(self):
        # RULES widget
        highscore_widget = QWidget(self.central_widget)
        highscore_widget.setObjectName("highscore_widget")
        highscore_widget.setMaximumSize(642, 344)

        self.widget = QWidget(highscore_widget)

        highscore_widget_layout = QVBoxLayout(highscore_widget)
        size_policy = QSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )
        highscore_widget.setSizePolicy(size_policy)

        highscore_table = QTableWidget()
        highscore_table.setSizePolicy(size_policy)
        datas = read_high_scores()
        highscore_table.setRowCount(10)
        # highscore_table.verticalHeader().setVisible(False)
        highscore_table.setColumnCount(6)
        highscore_table.setHorizontalHeaderLabels(
            ["Name", "Effective", "Turns", "Game Time", "Date", "SCORES"]
        )
        # highscore_table.setSortingEnabled(True)

        for row, data in enumerate(datas):
            for column, value in enumerate(data.values()):
                item = QTableWidgetItem(str(value))
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                highscore_table.setItem(row, column, item)

        # palette = highscore_table.palette()
        # palette.setColor(QPalette.ColorRole.Base, QColor('yellow'))
        # highscore_table.setPalette(palette)

        highscore_widget_layout.addWidget(highscore_table)
        # highscore_widget_layout.setStretchFactor(highscore_table, 1)

        # nav
        nav_widget = QWidget(self.central_widget)
        nav_widget.setMaximumSize(200, 300)
        widget = QWidget(nav_widget)
        nav_layout = QVBoxLayout(widget)
        delete_button = QPushButton(
            "Delete Highscores",
            clicked=lambda: [
                self.delete_accept(
                    reset_high_scores,
                    "DELETE highscores?!",
                    "Are you sure You want to DELETE all Highscores??",
                ),
                self.highscores_layout(),
            ],
        )
        back_game_button = QPushButton(
            "<- Back to Game", clicked=self.start_battle_layout
        )
        if get_value_from_game_statistics("player_ships") == 0:
            back_game_button.setEnabled(False)
        back_menu_button = QPushButton("<- Back to Menu", clicked=self.main_menu_layout)
        self.buttons(delete_button)
        self.buttons(back_game_button)
        self.buttons(back_menu_button)
        spacer = QSpacerItem(
            20, 400, QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Expanding
        )
        nav_layout.addItem(spacer)
        nav_layout.addWidget(delete_button)
        nav_layout.addWidget(back_game_button)
        nav_layout.addWidget(back_menu_button)
        nav_widget.setLayout(nav_layout)
        nav_layout.setSpacing(0)

        j = QWidget()
        main_layout = QHBoxLayout(j)
        main_layout.addWidget(highscore_widget)
        main_layout.addWidget(nav_widget)
        # dodawanie głównego widgeta do QStackedLayout
        self.stacked_layout.addWidget(j)
        self.stacked_layout.setCurrentWidget(j)

    def stat(self):
        """Method responsible for refreshing statistics displayed on the screen."""

        self.player_statistic_1.setText(
            f"Ships: {get_value_from_game_statistics('player_ships')}"
        )
        self.player_statistic_2.setText(
            f"Available Shots: {get_value_from_game_statistics('player_available_shots')}"
        )
        self.player_statistic_3.setText(
            f"Shots (All): {get_value_from_game_statistics('player_shots')}"
        )
        self.player_statistic_4.setText(
            f"Hit Shots: {get_value_from_game_statistics('player_hit')}"
        )
        self.player_statistic_5.setText(
            f"Missed Shots: {get_value_from_game_statistics('player_missed')}"
        )
        self.player_statistic_6.setText(
            f"Effective: {get_value_from_game_statistics('player_effective')}"
        )

        self.cpu_statistic_1.setText(
            f"Ships: {get_value_from_game_statistics('cpu_ships')}"
        )
        self.cpu_statistic_2.setText(
            f"Available Shots: {get_value_from_game_statistics('cpu_available_shots')}"
        )
        self.cpu_statistic_3.setText(
            f"Shots (All): {get_value_from_game_statistics('cpu_shots')}"
        )
        self.cpu_statistic_4.setText(
            f"Hit Shots: {get_value_from_game_statistics('cpu_hit')}"
        )
        self.cpu_statistic_5.setText(
            f"Missed Shots: {get_value_from_game_statistics('cpu_missed')}"
        )
        self.cpu_statistic_6.setText(
            f"Effective: {get_value_from_game_statistics('cpu_effective')}"
        )

    def buttons(self, button):
        button.setObjectName("button")
        button.setFixedSize(130, 30)
        button.setFont(QFont("Arial", 10))
        button.enterEvent = lambda event, btn=button: btn.setFont(
            QFont("Arial", 10, italic=True)
        )
        button.leaveEvent = lambda event, btn=button: btn.setFont(QFont("Arial", 10))
        if button.text() == "":
            button.setEnabled(False)

    def delete_accept(self, func, title, message):
        """Method that requires confirmation to perform a specific task."""
        sound = QSoundEffect()
        try:
            sound.setSource(
                QUrl.fromLocalFile("C:/Windows/Media/Windows Critical Stop.wav")
            )
            sound.play()
        except:
            pass
        reply = QMessageBox.warning(
            self,
            f"{title}",
            f"{message}",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if reply == QMessageBox.StandardButton.Yes:
            func()

    def sea_zone(self, who, who_grid):
        """Method responsible for creating a board for selected side."""
        board = get_board_from_boards(who, self.widget)
        for i in range(10):
            row = []
            for j in range(10):
                zone = board[int(f"{i}{j}")]
                who_grid.addWidget(zone, i, j)
            board.extend(row)
        return board

    def player_turn(self):
        player_available_shots = ceil(
            get_value_from_game_statistics("player_ships") * 0.5
        )
        update_game_statistics_table("player_available_shots", player_available_shots)
        self.stat()
        calculate_value_from_game_statistic("turns", 1)

    def cpu_turn(self):
        cpu_avaiable_shots = ceil(get_value_from_game_statistics("cpu_ships") * 0.5)
        update_game_statistics_table("cpu_available_shots", cpu_avaiable_shots)
        i = 0
        i_max = get_value_from_game_statistics("cpu_available_shots")
        while i < i_max:
            random_zone = random.randint(0, 99)
            if str(random_zone) in get_zones("shot") or str(random_zone) in get_zones(
                "fire"
            ):
                continue
            update_zones("shot", random_zone)
            i += 1
            self.shot("cpu", random_zone, None)
        self.stat()
        self.player_turn()

    def check_coordinate(self, who: str, checking_zone: int, move: str):
        """Method validates the selected zone depending on the situation. The main assumptions are: the ship cannot stand next to the ship. Return 'bool'."""

        # cases of zones
        top_left_corner = (1, 10, 11)  # if zone 0
        top_side = (-1, 1, 9, 10, 11)  # if zones from 1 to 8 every 1
        top_right_corner = (-1, 9, 10)  # if zone 9
        right_side = (-11, -10, -1, 9, 10)  # if zones from 19 to 89 every 10
        bottom_right_corner = (-11, -10, -1)  # if zone 99
        bottom_side = (-11, -10, -9, -1, 1)  # if zones from 91 to 98 every 1
        bottom_left_corner = (-10, -9, 1)  # if zone 90
        left_side = (-10, -9, 1, 10, 11)  # if zones from 10 to 80 every 10
        inside = (-11, -10, -9, -1, 1, 9, 10, 11)  # if rest of cases
        ship_image = QPixmap("data\images\game\ship1.png").scaled(QSize(30, 30))

        # in SENDING ships (move = 'ship')
        if checking_zone == 0:
            for i in top_left_corner:
                if (
                    get_zone_from_boards(who, checking_zone + i)
                    .pixmap(
                        get_zone_from_boards(who, checking_zone + i).availableSizes()[0]
                    )
                    .toImage()
                    == ship_image.toImage()
                ):
                    # print(f'{checking_zone} Too close ship in {checking_zone + i} zone')
                    # self.action.setText('Too close another Ship!')
                    return False
        elif checking_zone in tuple(range(1, 9)):
            for i in top_side:
                if (
                    get_zone_from_boards(who, checking_zone + i)
                    .pixmap(
                        get_zone_from_boards(who, checking_zone + i).availableSizes()[0]
                    )
                    .toImage()
                    == ship_image.toImage()
                ):
                    # print(f'{checking_zone} Too close ship in {checking_zone + i} zone')
                    return False
        elif checking_zone == 9:
            for i in top_right_corner:
                if (
                    get_zone_from_boards(who, checking_zone + i)
                    .pixmap(
                        get_zone_from_boards(who, checking_zone + i).availableSizes()[0]
                    )
                    .toImage()
                    == ship_image.toImage()
                ):
                    # print(f'{checking_zone} Too close ship in {checking_zone + i} zone')
                    return False
        elif checking_zone in tuple(range(19, 90, 10)):
            for i in right_side:
                if (
                    get_zone_from_boards(who, checking_zone + i)
                    .pixmap(
                        get_zone_from_boards(who, checking_zone + i).availableSizes()[0]
                    )
                    .toImage()
                    == ship_image.toImage()
                ):
                    # print(f'{checking_zone} Too close ship in {checking_zone + i} zone')
                    return False
        elif checking_zone == 99:
            for i in bottom_right_corner:
                if (
                    get_zone_from_boards(who, checking_zone + i)
                    .pixmap(
                        get_zone_from_boards(who, checking_zone + i).availableSizes()[0]
                    )
                    .toImage()
                    == ship_image.toImage()
                ):
                    # print(f'{checking_zone} Too close ship in {checking_zone + i} zone')
                    return False
        elif checking_zone in tuple(range(91, 99)):
            for i in bottom_side:
                if (
                    get_zone_from_boards(who, checking_zone + i)
                    .pixmap(
                        get_zone_from_boards(who, checking_zone + i).availableSizes()[0]
                    )
                    .toImage()
                    == ship_image.toImage()
                ):
                    # print(f'{checking_zone} Too close ship in {checking_zone + i} zone')
                    return False
        elif checking_zone == 90:
            for i in bottom_left_corner:
                if (
                    get_zone_from_boards(who, checking_zone + i)
                    .pixmap(
                        get_zone_from_boards(who, checking_zone + i).availableSizes()[0]
                    )
                    .toImage()
                    == ship_image.toImage()
                ):
                    # print(f'{checking_zone} Too close ship in {checking_zone + i} zone')
                    return False
        elif checking_zone in tuple(range(10, 90, 10)):
            for i in left_side:
                if (
                    get_zone_from_boards(who, checking_zone + i)
                    .pixmap(
                        get_zone_from_boards(who, checking_zone + i).availableSizes()[0]
                    )
                    .toImage()
                    == ship_image.toImage()
                ):
                    # print(f'{checking_zone} Too close ship in {checking_zone + i} zone')
                    return False
        else:
            for i in inside:
                if (
                    get_zone_from_boards(who, checking_zone + i)
                    .pixmap(
                        get_zone_from_boards(who, checking_zone + i).availableSizes()[0]
                    )
                    .toImage()
                    == ship_image.toImage()
                ):
                    # print(f'{checking_zone} Too close ship in {checking_zone + i} zone')
                    return False

    def shot(self, who: str, zone: int, widget, *args):
        calculate_value_from_game_statistic(f"{who}_shots", 1)
        calculate_value_from_game_statistic(f"{who}_available_shots", -1)
        sea_image = QPixmap("data\images\game\sea.png").scaled(QSize(30, 30))
        ship_image = QPixmap("data\images\game\ship1.png").scaled(QSize(30, 30))
        fire_image = QPixmap("data/images/game/fire1.png").scaled(QSize(30, 30))
        shot_image = QPixmap("data\images\game\missed1.png").scaled(QSize(30, 30))

        if who == "player":
            check = checking_zone_brom_board("cpu", zone)
            if check == "fire":
                widget.setIcon(QIcon(fire_image))
                calculate_value_from_game_statistic(f"player_hit", 1)
                calculate_value_from_game_statistic(f"cpu_ships", -1)
                self.music_and_sounds("sound", "hit_start")
            elif check == "shot":
                widget.setIcon(QIcon(shot_image))
                calculate_value_from_game_statistic(f"player_missed", 1)
                self.music_and_sounds("sound", "shot_start")

            if get_value_from_game_statistics("player_available_shots") == 0:
                self.cpu_turn()

        elif who == "cpu":
            check = checking_zone_brom_board("player", zone)
            if check == "fire":
                self.player_board[zone].setIcon(QIcon(fire_image))
                calculate_value_from_game_statistic(f"cpu_hit", 1)
                calculate_value_from_game_statistic(f"player_ships", -1)
                self.music_and_sounds("sound", "hit_start")
            elif check == "shot":
                self.player_board[zone].setIcon(QIcon(shot_image))
                calculate_value_from_game_statistic(f"cpu_missed", 1)
                self.music_and_sounds("sound", "shot_start")

        if get_value_from_game_statistics("player_ships") == 0:
            self.end_game("cpu")
            return
        elif get_value_from_game_statistics("cpu_ships") == 0:
            self.end_game("player")
            return

        self.stat()

    def end_game(self, winner: str):
        self.end_time_game = time.time()
        self.total_time_game = (
            str(round((self.end_time_game - self.start_time_game) / 60, 2)) + " min."
        )
        for i in range(0, 100):
            try:
                get_zone_from_boards('cpu', i, winner=True)
                self.cpu_board[i].disconnect()
            except TypeError:
                pass

        self.stat()

        add_high_scores(winner, self.total_time_game)

    def ship(self, who: str, zone: int, *args):
        """Method responsible for the correct placement of ships an the board."""

        if self.check_coordinate(who, zone, "ship") == False:
            return

        # mam nr zone, pobieram aktualny stan ikony
        checking_zone_icon = get_zone_from_boards(who, zone)
        sea_image = QPixmap("data\images\game\sea.png").scaled(QSize(30, 30))
        ship_image = QPixmap("data\images\game\ship1.png").scaled(QSize(30, 30))
        if (
            checking_zone_icon.pixmap(checking_zone_icon.availableSizes()[0]).toImage()
            == sea_image.toImage()
        ):
            if self.level_game(who) == get_value_from_game_statistics(f"{who}_ships"):
                return
            update_boards_table(who, "ship", zone)
            calculate_value_from_game_statistic(f"{who}_ships", 1)
        elif (
            checking_zone_icon.pixmap(checking_zone_icon.availableSizes()[0]).toImage()
            == ship_image.toImage()
        ):
            update_boards_table(who, "sea", zone)
            calculate_value_from_game_statistic(f"{who}_ships", -1)

        try:
            if args[0]:
                self.player_fleet_layout()
        except IndexError:
            pass

    def random_fleet(self, who: str):
        """Method responsible for randomly placing ships on boards of both sides."""
        while get_value_from_game_statistics(f"{who}_ships") < self.level_game(who):
            random_zone = random.randint(0, 99)
            if who == "player":
                self.ship(who="player", zone=random_zone)
            elif who == "cpu":
                self.ship(who="cpu", zone=random_zone)
        self.main_info.setText("Random fleets send!")

    def clear_player_board(self):
        """Method clear the player's board."""
        for zone_num in range(0, 100):
            update_boards_table("player", "sea", zone_num)
        update_game_statistics_table("player_ships", 0)
        self.player_fleet_layout()
        # self.stat()

    def level_game(self, who: str):
        level = get_value_from_game_statistics("level")
        max_ships = get_value_from_game_statistics("all_ships")
        if level == "Normal":
            return max_ships
        elif level == "Easy":
            player_max_ships = max_ships + 1
            cpu_max_ships = max_ships
            if who == "player":
                return player_max_ships
            elif who == "cpu":
                return cpu_max_ships
        elif level == "Hard":
            player_max_ships = max_ships
            cpu_max_ships = max_ships + 1
            if who == "player":
                return player_max_ships
            elif who == "cpu":
                return cpu_max_ships

    def reset_game(self):
        """Method responsible for restoring game settings to the starting settings, without having to restart the application."""
        self.main_menu_buttons_list[0].setText("Start Battle")
        self.main_menu_buttons_list[1].setEnabled(True)
        self.main_menu_buttons_list[2].setEnabled(True)
        self.main_menu_buttons_list[3].setEnabled(True)
        for zone in range(0, 100):
            update_boards_table("player", "sea", zone)
            update_boards_table("cpu", "sea", zone)
        game_statistics_table_default()
        self.main_info.setText("All game settings have been reset!")

        # timer = QTimer()
        # timer.timeout.connect(lambda: self.main_info.setText('załatwione'))
        # timer.start(1000)

    def music_and_sounds(self, sound=None, action=None, stan=None):
        # MUSIC music
        if sound == "music":
            if stan is not None:
                update_game_statistics_table("music", stan)

            if stan == 1:
                main_music.main_music_start()
            elif stan == 0:
                main_music.main_music_stop()

        # SOUNDS hit, shot, sea
        if sound == "sound":
            if stan is not None:
                update_game_statistics_table("sounds", stan)

            play = get_value_from_game_statistics("sounds") == 1

            if action == "hit_start" and play:
                hit_sound.hit_sound_start()
            elif action == "shot_start" and play:
                shot_sound.shot_sound_start()
            elif action == "sea_start" and play:
                sea_sound.sea_sound_start()
            elif action == "sea_stop":
                sea_sound.sea_sound_stop()

    def resizeEvent(self, event):
        size_window = event.size()
        self.width = size_window.width()
        self.height = size_window.height()
        # for i in range(6):
        #     widget = QWidget()
        #     # widget.setMaximumSize(900, 650)
        #     x = (self.width - widget.width()) // 2
        #     y = (self.height - widget.height()) // 2
        #     widget.setGeometry(x, y, widget.width(), widget.height())
        #     self.stacked_layout.addWidget(widget)
        # print(self.width, self.height)

        # update size QGraphicsView when change window size
        # self.view.setSceneRect(self.view.rect())


# opening file with style sheets
with open("data/styles/styles.css", "r") as file:
    style_sheet = file.read()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()

    main_music = MainMusic()
    sea_sound = SeaSound()
    shot_sound = ShotSound()
    hit_sound = HitSound()

    if bool(get_value_from_game_statistics("music")):
        main_music.main_music_start()

    app.setStyleSheet(style_sheet)

    window.show()
    # window.showMaximized()

    sys.exit(app.exec())
