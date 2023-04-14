import os
import sqlite3

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
    c.execute("CREATE TABLE IF NOT EXISTS game_statistics (id INTEGER PRIMARY KEY, level STRING, all_ships INTEGER, turns INTEGER, player_name STRING, player_ships INTEGER, player_available_shots INTEGER, player_missed INTEGER, player_hit INTEGER, player_shots INTEGER, player_effective REAL, cpu_name STRING, cpu_ships INTEGER, cpu_available_shots INTEGER, cpu_missed INTEGER, cpu_hit INTEGER, cpu_shots INTEGER, cpu_effective REAL, shot_zones STRING, fire_zones STRING)")
    c.execute("INSERT INTO game_statistics (level, all_ships, turns, player_name, player_ships, player_available_shots, player_missed, player_hit, player_shots, player_effective, cpu_name, cpu_ships, cpu_available_shots, cpu_missed, cpu_hit, cpu_shots, cpu_effective, shot_zones, fire_zones) VALUES (:level, :all_ships, :turns, :player_name, :player_ships, :player_available_shots, :player_missed, :player_hit, :player_shots, :player_effective, :cpu_name, :cpu_ships, :cpu_available_shots, :cpu_missed, :cpu_hit, :cpu_shots, :cpu_effective, :shot_zones, :fire_zones)", 
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


# OPERATIONS on game_statistics table
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








# HIGH_SCORES table
def high_scores_table_default():
    with sqlite3.connect('data\db\game.db') as conn:
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS high_scores (id INTEGER PRIMARY KEY, player_name TEXT, effective REAL, turns INTEGER, game_time TEXT, date DATE)''')

def add_high_scores(player_name: str, effective: str, turns: int, game_time: str, date: str):
    with sqlite3.connect('data\db\game.db') as conn:
        c = conn.cursor()
        c.execute("INSERT INTO high_scores (player_name, effective, turns, game_time, date) VALUES (:player_name, :effective, :turns, :game_time, :date)", 
            {
                'player_name': f"{player_name}", 
                'effective': f"{effective}",
                'turns': f"{turns}", 
                'game_time': f"{game_time}", 
                'date': f"{date}",
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
