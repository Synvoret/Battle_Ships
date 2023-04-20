import os
import sqlite3
import datetime
import json
import tempfile
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtGui import QPixmap, QIcon
from PyQt6.QtCore import QSize

# DATABASES
def create_db():
    '''Function responsible for creating a new database for game. It's task is to check if the base exists, if it does, it skips the task.'''
    if os.path.exists('data\db\game.db'):        
        return
    conn = sqlite3.connect('data\db\game.db')
    conn.close()




# GAME STATISTICS table
def game_statistics_table_default():
    '''Function resets the existing table and creates a new one with default settings for the game. Name for table is "game_statistics".'''
    conn = sqlite3.connect('data\db\game.db')
    c = conn.cursor()
    c.execute("DROP TABLE IF EXISTS game_statistics")
    c.execute('''CREATE TABLE IF NOT EXISTS game_statistics 
                (id INTEGER PRIMARY KEY, 
                level STRING, 
                all_ships INTEGER, 
                turns INTEGER, 
                player_name STRING, 
                player_ships INTEGER, 
                player_available_shots INTEGER, 
                player_missed INTEGER, 
                player_hit INTEGER, 
                player_shots INTEGER, 
                player_effective REAL, 
                cpu_name STRING, 
                cpu_ships INTEGER, 
                cpu_available_shots INTEGER, 
                cpu_missed INTEGER, 
                cpu_hit INTEGER, 
                cpu_shots INTEGER, 
                cpu_effective REAL, 
                shot_zones STRING, 
                fire_zones STRING)''')
    c.execute('''INSERT INTO game_statistics 
                (level, 
                all_ships, 
                turns, 
                player_name, 
                player_ships, 
                player_available_shots, 
                player_missed, 
                player_hit, 
                player_shots, 
                player_effective, 
                cpu_name, 
                cpu_ships, 
                cpu_available_shots, 
                cpu_missed, 
                cpu_hit, 
                cpu_shots, 
                cpu_effective, 
                shot_zones, 
                fire_zones) VALUES 
                (   
                    :level, 
                    :all_ships, 
                    :turns, 
                    :player_name, 
                    :player_ships, 
                    :player_available_shots, 
                    :player_missed, 
                    :player_hit, 
                    :player_shots, 
                    :player_effective, 
                    :cpu_name, 
                    :cpu_ships, 
                    :cpu_available_shots, 
                    :cpu_missed, 
                    :cpu_hit, 
                    :cpu_shots, 
                    :cpu_effective, 
                    :shot_zones, 
                    :fire_zones)''', 
                    {
                        'level': 'Normal', 
                        'all_ships': 4,
                        'turns': 0, 
                        'player_name': 'Player', 
                        'player_ships': 0, 
                        'player_available_shots': 0, 
                        'player_missed': 0, 
                        'player_hit': 0,
                        'player_shots': 0,
                        'player_effective': 0.0,
                        'cpu_name': 'CPU', 
                        'cpu_ships': 0, 
                        'cpu_available_shots': 0, 
                        'cpu_missed': 0, 
                        'cpu_hit': 0, 
                        'cpu_shots': 0,
                        'cpu_effective': 0.0,
                        "shot_zones": '',
                        "fire_zones": ''
                        })
    conn.commit()
    conn.close()

def update_game_statistics_table(column: str, data):
    conn = sqlite3.connect('data\db\game.db')    
    c = conn.cursor()
    c.execute(f"UPDATE game_statistics SET {column} = ? WHERE id = 1", (data, ))
    conn.commit()
    conn.close()

def calculate_value_from_game_statistic(column: str, value: int):
    conn = sqlite3.connect('data\db\game.db')
    c = conn.cursor()
    c.execute(f"SELECT {column} FROM game_statistics WHERE id = 1")
    current_value = c.fetchone()[0]
    new_value = current_value + value
    c.execute(f"UPDATE game_statistics SET {column} = ? WHERE id = 1", (new_value, ))
    conn.commit()
    conn.close()

def get_value_from_game_statistics(column: str):
    conn = sqlite3.connect('data\db\game.db')
    c = conn.cursor()
    c.execute(f"SELECT {column} FROM game_statistics WHERE id = 1")
    result = c.fetchone()
    value = result[0]
    if column == 'player_effective':
        try:
            value = str(round(get_value_from_game_statistics('player_hit') / get_value_from_game_statistics('player_shots') * 100, 2)) + " %"
        except ZeroDivisionError:
            value = "0 %"
    elif column == 'cpu_effective':
        try:
            value = str(round(get_value_from_game_statistics('cpu_hit') / get_value_from_game_statistics('cpu_shots') * 100, 2)) + " %"
        except ZeroDivisionError:
            value = "0 %"
    conn.close()
    return value

def read_all_values_from_game_statistics():
    conn = sqlite3.connect('data\db\game.db')
    c = conn.cursor()
    c.execute("SELECT * FROM game_statistics WHERE id=1")
    row = c.fetchone()
    columns = [description[0] for description in c.description]
    columns.remove('id')
    result = {}
    for i in range(len(columns)):
        result[columns[i]] = row[i + 1]
    return result

def update_zones(type: str, data: str):
    conn = sqlite3.connect('data\db\game.db')    
    c = conn.cursor()
    column = f"{type}_zones"
    c.execute(f"SELECT {column} FROM game_statistics WHERE id = 1")    
    current_data = c.fetchone()[0]
    if data != '-':
        new_data = f"{current_data} {data}"
    elif data == '-':
        new_data = f" "
    c.execute(f"UPDATE game_statistics SET {column} = ? WHERE id = 1", (new_data, ))
    conn.commit()
    conn.close()

def get_zones(type: str):
    conn = sqlite3.connect('data\db\game.db')
    c = conn.cursor()
    column = f"{type}_zones"
    c.execute(f"SELECT {column} FROM game_statistics WHERE id = 1")
    result = c.fetchone()
    value = str(result[0]).split()
    value = set(value)
    conn.close()
    return value







# BOARDS table
def make_new_boards_table():
    with sqlite3.connect('data/db/game.db') as conn:
        c = conn.cursor()
        c.execute("DROP TABLE IF EXISTS boards")
        c.execute('''CREATE TABLE boards 
                    (zone INTEGER PRIMARY KEY, 
                    player_board STRING,
                    cpu_board STRING)''')
        for i in range(1, 101):
            c.execute('''INSERT INTO boards
                        (player_board,
                        cpu_board) VALUES
                        (
                            :player_board,
                            :cpu_board)''',
                            {
                                'player_board': 'sea',
                                'cpu_board': 'sea'
                            })

def update_boards_table(who: str, types: str, zone: int):
    '''Method that updates the situation on both sides' boards. As arguments it requires:
        - who: which side is update (player, cpu),
        - types: update situation at zone (sea, ship, shot, fire)
        - zones: choose zone, from 1 to 100.\n
        For example: update_boards_table('player', 'ship', 10)'''
    with sqlite3.connect('data/db/game.db') as conn:
        c = conn.cursor()
        column = f"{who}_board"
        type_zone = types
        c.execute(f"SELECT {column} FROM boards WHERE zone=?", (f"{zone}",))
        sit = 'sea'
        if type_zone == 'ship':
            sit = 'ship'
        elif type_zone == 'sea':
            sit = 'sea'
        elif type_zone == 'fire':
            sit = 'fire'
        elif type_zone == 'shot':
            sit = 'shot'
        c.execute(f"UPDATE boards SET {column} = ? WHERE zone = ?", (f"{sit}", f"{zone}"))

def get_zone_from_boards(who: str, zone: int):
    with sqlite3.connect('data/db/game.db') as conn:
        c = conn.cursor()
        column = f"{who}_board"
        c.execute(f"SELECT {column} FROM boards WHERE zone=?", (f"{zone}",))
        row = c.fetchone()[0]
        pixmap = QPixmap()
        
        if row == 'sea':
            pixmap = QPixmap('data\images\game\sea.png').scaled(QSize(30, 30))
            sit = 'sea'
        elif row == 'ship':
            pixmap = QPixmap('data\images\game\ship1.png').scaled(QSize(30, 30))
            sit = 'ship'
        elif row == 'shot':
            pixmap = QPixmap('data\images\game\missed1.png').scaled(QSize(30, 30))
            sit = 'shot'
        elif row == 'fire':
            pixmap = QPixmap(r'data/images/game/fire1.png').scaled(QSize(30, 30))
            sit = 'fire'
        
        zone_icon = QIcon(pixmap)
        
        return zone_icon

def get_board_from_boards(who: str, parent):
    board = []
            
    for i in range(10):
        row = []
        for j in range(10):
            zone_num = i * 10 + j + 1
            zone_icon = get_zone_from_boards(who, zone_num)
            locals()['btn{i}{j}'] = row.append(QPushButton(parent=parent))
            btn = row[int(f"{j}")]
            btn.setStyleSheet("background-color: rgb(200, 200, 200)")
            btn.setMouseTracking(True)
            btn.setIcon(zone_icon)
            btn.setIconSize(QSize(30, 30))
            # btn.enterEvent = lambda event, btn=btn: btn.setStyleSheet("background-color: #00C6F7")
            # btn.leaveEvent = lambda event, btn=btn: btn.setStyleSheet("background-color: rgb(200, 200, 200)")
        board.extend(row)
    return board

def checking_zone_brom_board(who: str, zone: int):
    with sqlite3.connect('data/db/game.db') as conn:
        c = conn.cursor()
        column = f"{who}_board"
        c.execute(f"SELECT {column} FROM boards WHERE zone=?", (f"{zone}",))
        sit = c.fetchone()[0]
        # print(sit, zone, who)
        if sit == 'ship':
            update_boards_table(who, 'fire', zone)
            return 'fire'
        elif sit == 'sea':
            update_boards_table(who, 'shot', zone)
            return 'shot'
        elif sit == 'fire':
            return
        elif sit == 'shot':
            return 'shot'






# SAVE and LOAD GAME table
def save_game_table_default():
    with sqlite3.connect('data/db/game.db') as conn:
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS save_games (id INTEGER PRIMARY KEY, name_save STRING, file BLOB)''')

def save_file(name: str, data_to_write: dict):
    dane_json = json.dumps(data_to_write)
    # checking name_save
    with sqlite3.connect('data/db/game.db') as conn:
        c = conn.cursor()
        result = c.execute(f"SELECT * FROM save_games WHERE name_save LIKE '%{name}%'")
        if result.fetchone() is None:
            # when name not exist in db
            pass
        else:
            # when name exist in db
            return False
    
    # writing
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp_file:
        json.dump(data_to_write, temp_file)
        temp_file.flush()
    with sqlite3.connect('data/db/game.db') as conn:
        c = conn.cursor()
        with open(temp_file.name, 'r') as f:
            file_content = f.read()
        c.execute("INSERT INTO save_games (name_save, file) VALUES (:name_save, :file)",
                    {
                        'name_save': name,
                        'file': file_content
                    })

def load_file(name_save: str):
    with sqlite3.connect('data\db\game.db') as conn:
        c = conn.cursor()
        c.execute("SELECT file FROM save_games WHERE name_save=?", (name_save, ))
        results = c.fetchall()
        if results is None:
            print('nie ma takiego pliku')
        data = json.loads(results[0][0])
    return data

def read_files_list():
    with sqlite3.connect('data\db\game.db') as conn:
        c = conn.cursor()
        c.execute("SELECT name_save FROM save_games")
        results = c.fetchall()
    return results

def delete_file(name_save: str):
    with sqlite3.connect('data\db\game.db') as conn:
        c = conn.cursor()
        c.execute(f"DELETE FROM save_games WHERE name_save = '{name_save}'; ")








# HIGH_SCORES table
def high_scores_table_default():
    with sqlite3.connect('data\db\game.db') as conn:
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS high_scores (id INTEGER PRIMARY KEY, player_name TEXT, effective REAL, turns INTEGER, game_time TEXT, date DATE)''')

def add_high_scores(player_name: str, effective: str, turns: int, game_time: str):
    with sqlite3.connect('data\db\game.db') as conn:
        c = conn.cursor()
        c.execute("INSERT INTO high_scores (player_name, effective, turns, game_time, date) VALUES (:player_name, :effective, :turns, :game_time, :date)", 
                    {
                        'player_name': f"{player_name}", 
                        'effective': f"{effective}",
                        'turns': f"{turns}", 
                        'game_time': f"{game_time}", 
                        'date': datetime.date.today(),
                    })

def labels():
    with sqlite3.connect('data\db\game.db') as conn:
        c = conn.cursor()
        c.execute("PRAGMA table_info(high_scores)")
        column_names = [row[1].replace('_', ' ').title() for row in c.fetchall()]
    return column_names

def read_high_scores():
    with sqlite3.connect('data\db\game.db') as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM high_scores")
        column_names = [description[0].replace('_', ' ').title() for description in c.description]
        rows = []
        for row in c.fetchall():
            row_dict = {}
            for i, column_name in enumerate(column_names):
                row_dict[column_name] = row[i]
            rows.append(row_dict)
    return rows

def reset_high_scores():
    with sqlite3.connect('data\db\game.db') as conn:
        c = conn.cursor()
        c.execute("DELETE FROM high_scores")
