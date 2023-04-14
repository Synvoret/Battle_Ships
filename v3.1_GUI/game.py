import random
import tkinter as tk
from math import ceil
from tkinter import messagebox
from data.db import *

try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except:
    pass

# create db with default game statistics
create_db()
game_statistics_table_default()

COLOR = "#375362"

class Zone(tk.Button):
    def __init__(self, who, row: int, col: int):
        self.master = who
        self.row = row
        self.column = col
        self.image = sea_image
        super().__init__(bd=0.5, master=self.master, cursor="target", state="disabled", highlightthickness=0,
                         image=self.image)  # highlightthickness=0, relief="ridge",
        # super().__init__(bd=0.5, master=self.master, cursor="hand2", state="disabled", highlightthickness=0, image=self.image) # for ttk.Button
        self.grid(row=self.row, column=self.column)

    def check_coordinate(self, who: str, checking_zone: int, move: str):
        self.who = who
        self.checking_zone = checking_zone
        self.move = move  # place "ship" or "shot"

        top_left_corner = (1, 10, 11)  # 0
        top_side = (-1, 1, 9, 10, 11 ) # from 1 to 8 every 1
        top_right_corner = (-1, 9, 10)  # 9
        right_side = (-11, -10, -1, 9, 10)  # from 19 to 89 every 10
        bottom_right_corner = (-11, -10, -1 ) # 99
        bottom_side = (-11, -10, -9, -1, 1)  # # from 91 to 98 every 1
        bottom_left_corner = (-10, -9, 1)  # 90
        left_side = (-10, -9, 1, 10, 11)  # from 10 to 80 every 10
        inside = (-11, -10, -9, -1, 1, 9, 10, 11)  # rest of cases

        around_zones = {
            "top_left_corner": (1, 10, 11),  # 0
            "top_side": (-1, 1, 9, 10, 11),  # from 1 to 8 every 1
            "top_right_corner": (-1, 9, 10),  # 9
            "right_side": (-11, -10, -1, 9, 10),  # from 19 to 89 every 10
            "bottom_right_corner": (-11, -10, -1),  # 99
            "bottom_side": (-11, -10, -9, -1, 1),  # # from 91 to 98 every 1
            "bottom_left_corner": (-10, -9, 1),  # 90
            "left_side": (-10, -9, 1, 10, 11),  # from 10 to 80 every 10
            "inside": (-11, -10, -9, -1, 1, 9, 10, 11),  # rest of cases
        }

        def inside_zones() -> set:  # all zone without top, left, bottom and right edges
            x = set()
            for i in range(10, 81, 10):
                for j in range(1, 9):
                    x.add(i + j)
            return x
        # xxx = {i+j for i in range(10, 81, 10) for j in range(1, 9)}

        zones = {
            "top_left_corner": 0,  # 0
            "top_side": tuple(i for i in range(1, 9)),  # from 1 to 8 every 1
            "top_right_corner": 9,  # 9
            "right_side": tuple(i for i in range(19, 90, 10)),  # from 19 to 89 every 10
            "bottom_right_corner": 99,  # 99
            "bottom_side": tuple(i for i in range(91, 99, 1)),  # # from 91 to 98 every 1
            "bottom_left_corner": 90,  # 90
            "left_side": tuple(i for i in range(10, 81, 10)),  # from 10 to 80 every 10
            "inside": inside_zones(),  # rest of cases
        }

        # board
        board = []
        if self.who == 'player':
            board = player_board
        elif self.who == 'cpu':
            board = cpu_board

        # when sending Fleets (self.move = 'ship')
        if self.checking_zone == 0:
            for i in top_left_corner:
                if board[self.checking_zone + i]['image'] == "pyimage2":
                    message_area.itemconfig(message_text, text=f"Too close another Ship!")
                    return False
        elif self.checking_zone in range(1, 9):
            for i in top_side:
                if board[self.checking_zone + i]['image'] == "pyimage2":
                    message_area.itemconfig(message_text, text=f"Too close another Ship!")
                    return False
        elif self.checking_zone == 9:
            for i in top_right_corner:
                if board[self.checking_zone + i]['image'] == "pyimage2":
                    message_area.itemconfig(message_text, text=f"Too close another Ship!")
                    return False
        elif self.checking_zone in range(19, 90, 10):
            for i in right_side:
                if board[self.checking_zone + i]['image'] == "pyimage2":
                    message_area.itemconfig(message_text, text=f"Too close another Ship!")
                    return False
        elif self.checking_zone == 99:
            for i in bottom_right_corner:
                if board[self.checking_zone + i]['image'] == "pyimage2":
                    message_area.itemconfig(message_text, text=f"Too close another Ship!")
                    return False
        elif self.checking_zone in range(91, 99):
            for i in bottom_side:
                if board[self.checking_zone + i]['image'] == "pyimage2":
                    message_area.itemconfig(message_text, text=f"Too close another Ship!")
                    return False
        elif self.checking_zone == 90:
            for i in bottom_left_corner:
                if board[self.checking_zone + i]['image'] == "pyimage2":
                    message_area.itemconfig(message_text, text=f"Too close another Ship!")
                    return False
        elif self.checking_zone in range(10, 81, 10):
            for i in left_side:
                if board[self.checking_zone + i]['image'] == "pyimage2":
                    message_area.itemconfig(message_text, text=f"Too close another Ship!")
                    return False
        else:
            for i in inside:
                if board[self.checking_zone + i]['image'] == "pyimage2":
                    message_area.itemconfig(message_text, text=f"Too close another Ship!")
                    return False

    def ship(self, who: str, zone: int, *args: int):
        self.who = who
        self.zone = zone

        if self.check_coordinate(self.who, self.zone, "ship") == False:
            return

        try:
            self.max_ships = args[0]
        except:
            pass

        if self.who == 'player':
            if self.image == ship_image:
                self.image = sea_image
                self['image'] = sea_image
                calculate_value_from_game_statistic(f"{self.who}_ships", -1)
                message_area.itemconfig(message_text, text=f"You have turned back the Ship to port.")
            elif self.image == sea_image:
                if get_value_from_game_statistics(f"{self.who}_ships") == self.max_ships:
                    message_area.itemconfig(message_text, text=f"You have max. Ships.")
                    return
                self.image = ship_image
                self['image'] = ship_image
                calculate_value_from_game_statistic(f"{self.who}_ships", 1)
                message_area.itemconfig(message_text, text=f"You sent the Ship to sea.")

        if self.who == 'cpu':
            if self.image == ship_image_cpu:
                self.image = sea_image
                self['image'] = sea_image
                calculate_value_from_game_statistic(f"{self.who}_ships", -1)
            elif self.image == sea_image:
                self.image = ship_image_cpu
                self['image'] = ship_image_cpu
                calculate_value_from_game_statistic(f"{self.who}_ships", 1)

        stat()

    def sea(self, who: str):
        self.who = who
        if self.image != sea_image:
            self.image = sea_image
            self['image'] = sea_image
            update_game_statistics_table(f"{self.who}_ships", 0)
            update_game_statistics_table(f"{self.who}_available_shots", 0)
            stat()

    def shot(self, who: str):
        self.who = who

        calculate_value_from_game_statistic(f"{self.who}_shots", 1)
        calculate_value_from_game_statistic(f"{self.who}_available_shots", -1)

        if self.image == ship_image or self.image == ship_image_cpu:
            calculate_value_from_game_statistic(f"{self.who}_hit", 1)
            self.image = fire_image
            self['image'] = fire_image
            if self.who == 'player':
                calculate_value_from_game_statistic(f"cpu_ships", -1)
                if get_value_from_game_statistics('cpu_ships') == 0:
                    self.end_battle('player')
                    return False
            elif self.who == "cpu":
                calculate_value_from_game_statistic(f"player_ships", -1)
                # ....................... # wrzucenie pozycji trafionego statku do "fire_zones
                if get_value_from_game_statistics('player_ships') == 0:
                    self.end_battle('cpu')
                    return False
        elif self.image == fire_image or self.image == missed_image or self.image == sea_image:
            calculate_value_from_game_statistic(f"{self.who}_missed", 1)
            if self.image == fire_image:
                message_area.itemconfig(message_text,
                                        text=f"It's on fire, don't waste any ammo."
                                             f"\nSomething's on fire here, do you wanna hit it again?")
            elif self.image == missed_image:                
                message = get_value_from_game_statistics(f"{self.who}_name") + ", stupid shot :)" 
                message_area.itemconfig(message_text, text=message)
            elif self.image == sea_image:
                self.image = missed_image
                self['image'] = missed_image

        stat()

        if self.who == "cpu":
            pass
        elif get_value_from_game_statistics('player_available_shots') == 0:
            message_area.itemconfig(message_text, text=f"It was Your last shot in this turn!")
            for i in range(0, len(cpu_board)):
                cpu_board[i].config(command="")
            self.cpu_turn()

    def cpu_turn(self):
        stat()
        cpu_avaiable_shots = ceil(get_value_from_game_statistics('cpu_ships') * 0.5)
        update_game_statistics_table('cpu_available_shots', cpu_avaiable_shots)
        stat()
        i = 0
        i_max = get_value_from_game_statistics('cpu_available_shots')
        while i < i_max:
            cpu = random.randint(0, len(player_board) - 1)
            if str(cpu) in get_zones('shot') or cpu in get_zones('fire'):
                continue
            update_zones('shot', cpu)
            i += 1
            try:
                player_board[cpu].config(player_board[cpu].shot('cpu'))
            except TypeError:
                break
        stat()
        player_turn()

    def end_battle(self, who):
        for i in range(0, len(cpu_board)):
            player_board[i].config(command="")
            cpu_board[i].config(command="")
            if self.image == ship_image_cpu:
                cpu_board[i].config(image=sea_image)
        stat()
        turns = get_value_from_game_statistics('turns')
        message = get_value_from_game_statistics(f"{who}_name") + f" won after {turns} turns!"
        message_area.itemconfig(message_text, text=message)


def level_game(who: str):  # -> zwraca liczbę, ile ma być statków na stronę, maksymalna ilość statków
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

def sea_zone(who: str) -> list:
    board = []
    i = 0
    for j in range(0, 10):
        for k in range(0, 10):
            globals()['zone{}'.format(i)] = board.append(Zone(who, j, k))  # tworzenie wielu zmiennych w pętli
            i += 1
    print(globals())
    return board

def random_fleet(who: str):
    global player_board, cpu_board
    update_game_statistics_table(f"{who}_ships", 0)
    if who == 'player':
        player_board = sea_zone(player_sea_zone)
    elif who == 'cpu':
        cpu_board = sea_zone(cpu_sea_zone)

    while get_value_from_game_statistics(f'{who}_ships') < level_game(who):
        random_zone = random.randint(0, 99)
        if who == 'player':
            player_board[random_zone].config(
                command=player_board[random_zone].ship(who, random_zone, level_game(who)))
        elif who == 'cpu':
            cpu_board[random_zone].config(
                command=cpu_board[random_zone].ship(who, random_zone, level_game(who)))
        if get_value_from_game_statistics(f"{who}_ships") == level_game(who):
            break

    message_area.itemconfig(message_text, text="We sending random Fleets!!!")
    stat()


def clear_player_board():
    global player_board
    update_game_statistics_table('player_ships', 0)
    player_statistic1.config(text=f"Ships: {get_value_from_game_statistics('player_ships')}")
    player_board = sea_zone(player_sea_zone)
    message_area.itemconfig(message_text, text=f"Your Fleet is back!")


def player_fleet():
    global player_board
    message_area.itemconfig(message_text, text=f"Send Your Ships, {get_value_from_game_statistics('player_name')}")
    for i in range(0, len(player_board)):
        player_board[i].config(command=lambda x=player_board[i], y=i, z=level_game('player'): x.ship('player', y, z),
                               state="active")
    menu("disabled", None)
    stat()
    back_to_menu()


def player_turn():
    player_available_shots = ceil(get_value_from_game_statistics('player_ships') * 0.5)
    update_game_statistics_table('player_available_shots', player_available_shots)
    stat()
    calculate_value_from_game_statistic('turns', 1)
    if get_value_from_game_statistics('player_ships') == 0:
        return
    for i in range(0, len(cpu_board)):
        cpu_board[i].config(command=lambda x=cpu_board[i]: x.shot('player'))


def setup():
    menu("disabled", None)
    back_to_menu()

    def player_name_value():
        menu("disabled", None)
        back_to_setup()
        message_area.itemconfig(message_text, text="Max. 10 signs for Player Name.")
        entry_name = tk.Entry(menu_site, width=10, textvariable="", justify="center", highlightthickness=0)
        # entry_name.insert(0, "Your name?")
        entry_name.grid(row=0, column=0)
        entry_name.focus()

        def set_name():
            try:
                player_name.set(entry_name.get()[:10])
                entry_name.delete(0, "end")
            except ValueError:
                pass

        setup_1_1 = tk.Button(menu_site, text="Ok", cursor="hand2", command=set_name)
        setup_1_1.grid(row=1, column=0, sticky="NEWS")

    def ships_value():
        menu("disabled", None)
        back_to_setup()
        message_area.itemconfig(message_text, text=f"Max. 10 ships.")
        entry_ships = tk.StringVar(value=(get_value_from_game_statistics('all_ships')))
        entry_ships_spinbox = tk.Spinbox(menu_site, width=10, from_=1, to=10, increment=1, justify="center", textvariable=entry_ships)
        entry_ships_spinbox.grid(row=1, column=0)

        # entry_ships_spinbox.focus()

        def set_ships():
            if 0 < int(entry_ships.get()) < 11:
                update_game_statistics_table('all_ships', int(entry_ships.get()))
                stat()
            else:
                return

        setup_1_2 = tk.Button(menu_site, text="Ok", command=set_ships)
        setup_1_2.grid(row=2, column=0, sticky="NEWS")

    def level_value():
        menu("disabled", None)
        back_to_setup()

        def set_easy():
            update_game_statistics_table('level', 'Easy')
            message_area.itemconfig(message_text,
                                    text=f"You set level at EASY.\nNumber of Your ships is increased by one.")
            stat()

        setup_1_3 = tk.Button(menu_site, text="Easy", cursor='hand2', command=set_easy)
        setup_1_3.grid(row=1, column=0, sticky="NEWS")

        def set_normal():
            update_game_statistics_table('level', 'Normal')
            message_area.itemconfig(message_text, text=f"You set level at NORMAL")
            stat()

        setup_1_4 = tk.Button(menu_site, text="Normal", cursor='hand2', command=set_normal)
        setup_1_4.grid(row=2, column=0, sticky="NEWS")

        def set_hard():
            update_game_statistics_table('level', 'Hard')
            message_area.itemconfig(message_text,
                                    text=f"You set level at HARD.\nNumber of CPU ships is increased by one.")
            stat()

        setup_1_5 = tk.Button(menu_site, text="Hard", cursor='hand2', command=set_hard)
        setup_1_5.grid(row=3, column=0, sticky="NEWS")

    setup_1 = tk.Button(menu_site, text="Player Name", cursor="hand2", command=player_name_value)
    setup_1.grid(row=0, column=0, sticky="NEWS")
    setup_2 = tk.Button(menu_site, text="Ships", cursor="hand2", command=ships_value)
    setup_2.grid(row=1, column=0, sticky="NEWS")
    setup_3 = tk.Button(menu_site, text="Level", cursor="hand2", command=level_value)
    setup_3.grid(row=2, column=0, sticky="NEWS")


def reset_game():
    global player_board, cpu_board
    player_board = sea_zone(player_sea_zone)
    cpu_board = sea_zone(cpu_sea_zone)
    game_statistics_table_default()
    player_title_zone.config(text=get_value_from_game_statistics('player_name'))
    message_area.itemconfig(message_text, text="Reset ALL!!!")
    stat()


def start_battle():
    global player_board, cpu_board
    # restart battle statistics
    statistics_to_restart = ['turns', 'player_available_shots', 'player_missed', 'player_hit', 'player_shots', 'cpu_shots', 'cpu_available_shots', 'cpu_missed', 'cpu_hit', 'cpu_shots', 'shot_zones']
    for statistic in statistics_to_restart:
        if statistic != 'shot_zones':
            update_game_statistics_table(statistic, 0)
        elif statistic == 'shot_zones':
            update_zones('shot', '-')
    to_restart_memory_player_board = player_board
    if get_value_from_game_statistics('player_ships') != level_game('player') or get_value_from_game_statistics('cpu_ships') != level_game('cpu'):
        message_area.itemconfig(message_text, text=f"Before the battle, send full Fleets!!!")
        return False
    else:
        message_area.itemconfig(message_text, text=f"Destroy Your Enemy!!! Shoot!")

    menu("disabled", None)
    back_to_menu()
    for i in range(0, len(player_board)):
        player_board[i].config(state="active")
        cpu_board[i].config(state="active")

    player_turn()  # kto zaczyna

    stat()

    def restart_battle():

        global player_board
        player_board = to_restart_memory_player_board

        update_game_statistics_table('cpu_ships', 0)
        while get_value_from_game_statistics('cpu_ships') < level_game('cpu'):
            cpu_random_zone = random.randint(0, len(cpu_board) - 1)
            cpu_board[cpu_random_zone].config(command=cpu_board[cpu_random_zone].ship('cpu', level_game('cpu')))
            if get_value_from_game_statistics('cpu_ships') == level_game('cpu'):
                break
        stat()

    def retreat_from_battle():
        for i in range(0, len(player_board)):
            player_board[i].config(command=player_board[i].sea('player'))
        back_menu()

    battle_1 = tk.Button(menu_site, text="Restart Battle", command=restart_battle, state="disabled")
    battle_1.grid(row=0, column=0, sticky="NEWS")
    battle_3 = tk.Button(menu_site, text="Retreat", command=retreat_from_battle)
    battle_3.grid(row=1, column=0, sticky="NEWS")


def random_battle():
    reset_game()
    random_fleet()
    for i in range(0, len(player_board)):
        player_board[i].config(state="active")
        cpu_board[i].config(state="active")

    while get_value_from_game_statistics('player_ships') != 0 or get_value_from_game_statistics('cpu_ships') != 0:

        cpu_avaiable_shots = ceil(get_value_from_game_statistics('cpu_ships') * 0.5)
        update_game_statistics_table('cpu_available_shots', cpu_avaiable_shots)
        for i in range(0, get_value_from_game_statistics('cpu_available_shots')):
            cpu = random.randint(0, len(player_board) - 1)
            player_board[cpu].config(player_board[cpu].shot('cpu'))

        player_avaiable_shots = ceil(get_value_from_game_statistics('player_ships') * 0.5)
        update_game_statistics_table('player_available_shots', player_avaiable_shots)
        for i in range(0, get_value_from_game_statistics('player_available_shots')):
            cpu = random.randint(0, len(player_board) - 1)
            cpu_board[cpu].config(cpu_board[cpu].shot('player'))

    stat()


def menu(*args):
    global menu_site

    menu_site = tk.Frame(root, padx=20, pady=20, bg=COLOR)
    menu_site.grid(row=0, column=2, sticky="N")
    menu_1 = tk.Button(menu_site, text="Start Battle", cursor=args[1], command=start_battle, state=args[0])
    menu_1.grid(row=0, column=0, sticky="NEWS")
    menu_2 = tk.Button(menu_site, text="Player Fleet", cursor=args[1], command=player_fleet, state=args[0])
    menu_2.grid(row=1, column=0, sticky="NEWS")
    menu_3 = tk.Button(menu_site, text="Random Fleets", cursor=args[1],
                       command=lambda: [random_fleet('player'), random_fleet('cpu')], state=args[0])
    menu_3.grid(row=2, column=0, sticky="NEWS")
    menu_4 = tk.Button(menu_site, text="Clear Player Board", cursor=args[1], command=clear_player_board, state=args[0])
    menu_4.grid(row=3, column=0, sticky="NEWS")
    menu_6 = tk.Button(menu_site, text="Setup Game", cursor=args[1], command=setup, state=args[0])
    menu_6.grid(row=4, column=0, sticky="NEWS")
    menu_7 = tk.Button(menu_site, text="Reset Game", cursor=args[1], command=reset_game, state=args[0])
    menu_7.grid(row=5, column=0, sticky="NEWS")
    menu_10 = tk.Button(menu_site, text="Quit game", cursor=args[1], command=root.destroy, state=args[0])
    menu_10.grid(row=8, column=0, sticky="NEWS")


def stat():
    global player_statistic1

    player_statistic1.config(text=f"Ships: {get_value_from_game_statistics('player_ships')}")
    player_statistic2.config(text=f"Available Shots: {get_value_from_game_statistics('player_available_shots')}")
    player_statistic3.config(text=f"Shots (All): {get_value_from_game_statistics('player_shots')}")
    player_statistic4.config(text=f"Hit Shots: {get_value_from_game_statistics('player_hit')}")
    player_statistic5.config(text=f"Missed Shots: {get_value_from_game_statistics('player_missed')}")
    player_statistic6.config(text=f"Effective: {get_value_from_game_statistics('player_effective')}")

    cpu_statistic1.config(text=f"Ships: {get_value_from_game_statistics('cpu_ships')}")
    cpu_statistic2.config(text=f"Available Shots: {get_value_from_game_statistics('cpu_available_shots')}")
    cpu_statistic3.config(text=f"Shots (All): {get_value_from_game_statistics('cpu_shots')}")
    cpu_statistic4.config(text=f"Hit Shots: {get_value_from_game_statistics('cpu_hit')}")
    cpu_statistic5.config(text=f"Missed Shots: {get_value_from_game_statistics('cpu_missed')}")
    cpu_statistic6.config(text=f"Effective: {get_value_from_game_statistics('cpu_effective')}")

    game_stats0.config(text=f"Settings")
    game_stats1.config(text=f"Level: {get_value_from_game_statistics('level')}")
    game_stats2.config(text=f"Max. Ships: {get_value_from_game_statistics('all_ships')}")


def back_menu():
    menu(None, 'hand2')
    for i in range(0, len(player_board)):
        player_board[i].config(state="disabled")
        cpu_board[i].config(state="disabled")
    stat()

def back_to_menu():
    back_menu_button = tk.Button(menu_site, text="<- Back to Menu", cursor="hand2", command=back_menu)
    back_menu_button.grid(row=8, column=0, sticky="NEWS")
    stat()

def back_to_setup():
    back_menu_button = tk.Button(menu_site, text="<- Back to Setup", cursor="hand2", command=setup)
    back_menu_button.grid(row=8, column=0, sticky="NEWS")
    stat()


def about():
    messagebox.showinfo('Battle Ships v3.1',
                        'About Game:'
                        '\n\nDate: \t10 VI 2022'
                        '\nAuthor: \tLukasz Szabat'
                        '\nContact: \tsynvoret@gmail.com'
                        )


def rules():
    messagebox.showinfo('Battle Ships v3.1',
                        'Rules Game: v3.1'
                        '\n\nDefault amount ships:\t4'
                        '\nAvailable amount ships:\t1 - 10'
                        '\nDefault level:\t\tNormal'
                        '\nDifficulty levels:\t\tEasy, Normal, Hard'
                        '\nLevel rules:\t\tEasy -> Player +1 ship'
                        '\n\t\t\tHard -> CPU +1 ship'
                        '\nAvailable shots:\t\tActive ships / 2'
                        '\nShip by Ship: \t\tNo'
                        )


root = tk.Tk()
root.resizable(False, False)
root.title("Battle Ships v3.1")
root.config(bg=COLOR)
root.call('wm', 'iconphoto', root, tk.PhotoImage(file='images/fav.png'))

ship_image = tk.PhotoImage(file="images/ship1.png")
fire_image = tk.PhotoImage(file="images/fire1.png")
missed_image = tk.PhotoImage(file="images/missed1.png")
sea_image = tk.PhotoImage(file="images/sea.png")
ship_image_cpu = tk.PhotoImage(file="images/sea.png")

menubar = tk.Menu(root, background='#ff8000', foreground='black', activebackground='white', activeforeground='black')
root.config(menu=menubar)
file = tk.Menu(menubar, tearoff=0, foreground='black')
menubar.add_cascade(label="About", menu=file)
file.add_command(label="Rules", command=rules)
file.add_command(label="About", command=about)
file.add_separator()
file.add_command(label="Exit", command=root.destroy)

player_side = tk.Frame(padx=20, pady=20, bg=COLOR)
player_side.grid(row=0, column=0)
player_name = tk.StringVar(player_side, value=get_value_from_game_statistics('player_name'))
player_title_zone = tk.Label(player_side, textvariable=player_name, bg=COLOR, fg="white")
player_title_zone.grid(row=0, column=0)
player_sea_zone = tk.Frame(player_side)
player_sea_zone.grid(row=1, column=0)
player_board = sea_zone(player_sea_zone)

cpu_side = tk.Frame(root, padx=20, pady=20, bg=COLOR)
cpu_side.grid(row=0, column=1)
cpu_title_zone = tk.Label(cpu_side, text=get_value_from_game_statistics('cpu_name'), bg=COLOR, fg="white")
cpu_title_zone.grid(row=0, column=0)
cpu_sea_zone = tk.Frame(cpu_side)
cpu_sea_zone.grid(row=1, column=0)
cpu_board = sea_zone(cpu_sea_zone)

menu(None, "hand2")

player_statistic1 = tk.Label(player_side, text=f"Ships: {get_value_from_game_statistics('player_ships')}", bg=COLOR, foreground="white")
player_statistic1.grid(row=2, column=0, sticky="W")
player_statistic2 = tk.Label(player_side, text=f"Available Shots: {get_value_from_game_statistics('player_available_shots')}", bg=COLOR, foreground="white")
player_statistic2.grid(row=3, column=0, sticky="W")
player_statistic3 = tk.Label(player_side, text=f"Shots (All): {get_value_from_game_statistics('player_shots')}", bg=COLOR, foreground="white")
player_statistic3.grid(row=4, column=0, sticky="W")
player_statistic4 = tk.Label(player_side, text=f"Hit Shots: {get_value_from_game_statistics('player_hit')}", bg=COLOR, foreground="white")
player_statistic4.grid(row=5, column=0, sticky="W")
player_statistic5 = tk.Label(player_side, text=f"Missed Shots: {get_value_from_game_statistics('player_missed')}", bg=COLOR, foreground="white")
player_statistic5.grid(row=6, column=0, sticky="W")
player_statistic6 = tk.Label(player_side, text=f"Efective: {get_value_from_game_statistics('player_effective')}", bg=COLOR, foreground="white")
player_statistic6.grid(row=7, column=0, sticky="W")

cpu_statistic1 = tk.Label(cpu_side, text=f"Ships: {get_value_from_game_statistics('cpu_ships')}", bg=COLOR, foreground="white")
cpu_statistic1.grid(row=2, column=0, sticky="W")
cpu_statistic2 = tk.Label(cpu_side, text=f"Available Shots: {get_value_from_game_statistics('cpu_available_shots')}", bg=COLOR, foreground="white")
cpu_statistic2.grid(row=3, column=0, sticky="W")
cpu_statistic3 = tk.Label(cpu_side, text=f"Shots (All): {get_value_from_game_statistics('cpu_shots')}", bg=COLOR, foreground="white")
cpu_statistic3.grid(row=4, column=0, sticky="W")
cpu_statistic4 = tk.Label(cpu_side, text=f"Hit Shots: {get_value_from_game_statistics('cpu_hit')}", bg=COLOR, foreground="white")
cpu_statistic4.grid(row=5, column=0, sticky="W")
cpu_statistic5 = tk.Label(cpu_side, text=f"Missed Shots: {get_value_from_game_statistics('cpu_missed')}", bg=COLOR, foreground="white")
cpu_statistic5.grid(row=6, column=0, sticky="W")
cpu_statistic6 = tk.Label(cpu_side, text=f"Efective: {get_value_from_game_statistics('cpu_effective')}", bg=COLOR, foreground="white")
cpu_statistic6.grid(row=7, column=0, sticky="W")

game_stats0 = tk.Label(menu_site, bg=COLOR, foreground="white")
game_stats0.grid(row=9, column=0, sticky="WE")
game_stats1 = tk.Label(menu_site, text=f"Level: {get_value_from_game_statistics('level')}", bg=COLOR, foreground="white")
game_stats1.grid(row=10, column=0, sticky="W")
game_stats2 = tk.Label(menu_site, text=f"Max. Ships: {get_value_from_game_statistics('all_ships')}", bg=COLOR, foreground="white")
game_stats2.grid(row=11, column=0, sticky="W")

stat()
message_area = tk.Canvas(width=780, height=120, bg=COLOR)
message_text = message_area.create_text(400, 60, width=800, text="Battle Ships Game !!!", fill="white", font=("Arial", 10, "italic"))
message_area.grid(row=2, column=0, columnspan=2, padx=20, pady=20)

random_fleet('cpu')

if __name__ == '__main__':
    root.mainloop()