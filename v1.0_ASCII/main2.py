from datetime import datetime
from time import time, sleep
from typing import List # typowanie zmiennych

start_time = time()
from random import randint, choice
import ships
from string import ascii_lowercase
import os
import json

# Battle Ships at 10x10 seazone
board_player = [" "] * 100
board_cpu = [" "] * 100
board_cpu_hidden = [" "] * 100
game_statistic = {"all_ships": 4,
                  "player":
                    {"name": "Łukasz", "ships": 0, "parts_ships": 0, "missed": 0, "hit": 0, "shots": 0},
                  "cpu":
                    {"name": "CPU", "ships": 0, "parts_ships": 0, "missed": 0, "hit": 0, "shots": 0},
                  "turns": 0
                  }
X_AXIS = {"A": 0, "B": 1, "C": 2, "D": 3, "E": 4, "F": 5, "G": 6, "H": 7, "I": 8, "J": 9}
MENU = ("1 - Start Battle!", "2 - Player fleet", "3 - Random fleet", "4 - Clear Player Board", "5 - Show Statistic",
        "6 - Setup Game", "7 - Reset Game", "8 - Quit Game", "9 - Random: Fleets->Battle->Result->Exit", "", "")


def clear_screen():
  os.system('cls')
  return True


def save_highligsts(time):
  # argument time wygląda tak: "1.59 [s]", jest to czas z aktualnej gry
  date = datetime.now().strftime("%d." + "%m." + "%Y")
  new_data = {
    "game_time": {
      "date": date,
      "longest_playing_time": "0.00 [ms]"
    },
    "great_battle": {
      "date": date,
      "greatest_battle": ""}
    ,
    "most_shots": {
      "date": date,
      "most_shots_in_one_battle": 0
    },
  }
  try:  # nie zapisuje casu
    with open('highlights.json', "r") as highlights_file:
      # read old data file
      data = json.load(highlights_file)
      # check actual game_time with highlights game_time
      old_best_time = data['game_time']["longest_playing_time"]  # "1.67 [ms]"
      if "ms" in old_best_time:  # sprawdzam jednostkę czasu i przeliczam na sekundy
        old_best_time_in_seconds = float(old_best_time[:4]) / 1000
      elif "s" in old_best_time:
        old_best_time_in_seconds = float(old_best_time[:4])
      elif "min" in old_best_time:
        old_best_time_in_seconds = float(old_best_time[:4]) * 60
      elif "h" in old_best_time:
        old_best_time_in_seconds = float(old_best_time[:4]) * 3600
      if float(time[:4]) < old_best_time_in_seconds:  # porównuje nowy wynik z najlepszym
        pass
      elif float(time[:4]) > old_best_time_in_seconds:
        new_data["game_time"]["date"] = date
        new_data["game_time"]["longest_playing_time"] = time
  except FileNotFoundError:  # when file not found
    with open('highlights.json', "w") as highlights_file:
      json.dump(new_data, highlights_file, indent=4)
  else:
    # update old data with new data
    data.update(new_data)
    with open('highlights.json', "w") as highlights_file:
      # save old data with new data
      json.dump(data, highlights_file, indent=4)
  finally:
    pass
  # print("zapisałem statystyki")


def total_time_game():
  end_time = time()
  total_time = end_time - start_time
  ms = str(round(total_time * 1000, 2))
  s = str(round(total_time, 2))
  min = str(round(total_time * (1 / 60), 2))
  h = str(round(total_time * 0.00027777777777778, 2))
  showing_time = ""
  if total_time < 0.5:
    showing_time = "\nProgram time: " + ms + " [ms]"
    print(showing_time)
  elif total_time <= 60:
    showing_time = "\nProgram time: " + s + " [s]"
    print(showing_time)
  elif total_time <= 360:
    showing_time = "\nProgram time: " + min + " [min]"
    print(showing_time)
  elif total_time <= 1440:
    showing_time = "\nProgram time: " + h + " [h]"
    print(showing_time)
  # summary
  save_highligsts(showing_time[15:])


# PRINT ACTUAL SITUATION ON SEA
def board_print():
  i = 0
  print(f"BOARD - {game_statistic['player']['name']}".center(
    25) + "   " + f"BOARD - {game_statistic['cpu']['name']}".center(28) + "    " + f"MENU GAME".center(15))
  print(f"    A B C D E F G H I J " + "   " + f"      A B C D E F G H I J ")
  while i <= 9:
    if i < 9:
      print(
        f" {int(i + 1)} |{board_player[i * 10]}|{board_player[i * 10 + 1]}|{board_player[i * 10 + 2]}|{board_player[i * 10 + 3]}|{board_player[i * 10 + 4]}|{board_player[i * 10 + 5]}|{board_player[i * 10 + 6]}|{board_player[i * 10 + 7]}|{board_player[i * 10 + 8]}|{board_player[i * 10 + 9]}| {int(i + 1)}" + "   " + f" {int(i + 1)} |{board_cpu[i * 10]}|{board_cpu[i * 10 + 1]}|{board_cpu[i * 10 + 2]}|{board_cpu[i * 10 + 3]}|{board_cpu[i * 10 + 4]}|{board_cpu[i * 10 + 5]}|{board_cpu[i * 10 + 6]}|{board_cpu[i * 10 + 7]}|{board_cpu[i * 10 + 8]}|{board_cpu[i * 10 + 9]}| {int(i + 1)}" + "    " +
        MENU[i])
    elif i == 9:
      print(
        f"{int(i + 1)} |{board_player[i * 10]}|{board_player[i * 10 + 1]}|{board_player[i * 10 + 2]}|{board_player[i * 10 + 3]}|{board_player[i * 10 + 4]}|{board_player[i * 10 + 5]}|{board_player[i * 10 + 6]}|{board_player[i * 10 + 7]}|{board_player[i * 10 + 8]}|{board_player[i * 10 + 9]}| {int(i + 1)}" + "  " + f"{int(i + 1)} |{board_cpu[i * 10]}|{board_cpu[i * 10 + 1]}|{board_cpu[i * 10 + 2]}|{board_cpu[i * 10 + 3]}|{board_cpu[i * 10 + 4]}|{board_cpu[i * 10 + 5]}|{board_cpu[i * 10 + 6]}|{board_cpu[i * 10 + 7]}|{board_cpu[i * 10 + 8]}|{board_cpu[i * 10 + 9]}| {int(i + 1)}")
    i += 1
  print(f"    A B C D E F G H I J " + "   " + f"      A B C D E F G H I J ")
  # print(f"GAME STATISTIC. SHOTS: Player {game_statistic['player']['shots']}:{game_statistic['cpu']['shots']} CPU. HIT: Player {game_statistic['player']['hit']}:{game_statistic['cpu']['hit']} CPU. MISSED: Player {game_statistic['player']['missed']}:{game_statistic['cpu']['missed']} CPU. ")


def show_statistic():
  print(f"All ships: {game_statistic['all_ships']}"
        f"\nPlayer Name: {game_statistic['player']['name']}; Ships: {game_statistic['player']['ships']}; Shots: {game_statistic['player']['shots']} all/{game_statistic['player']['hit']} hits/{game_statistic['player']['missed']} missed; Parts ships: {game_statistic['player']['parts_ships']}"
        f"\nPlayer Name: {game_statistic['cpu']['name']}; Ships: {game_statistic['cpu']['ships']}; Shots: {game_statistic['cpu']['shots']} all/{game_statistic['cpu']['hit']} hits/{game_statistic['cpu']['missed']} missed; Parts ships: {game_statistic['cpu']['parts_ships']}")


def coordinate_random() -> str:
  ship_size = str(randint(1, 4))
  horizontal_axis = str(randint(1, 10))
  vertical_axis = choice(ascii_lowercase[:10])
  orientation_ship = choice(["h", "v"])
  # funkcja zwraca strina w postaci koordynatów, np "4a5h" lub "4a10v"
  return ship_size + vertical_axis + horizontal_axis + orientation_ship


def coordinate(size_ship: int, horizontal_axis: str, vertical_axis: str, orientation_ship: str, board: List[str], random: bool, who: str) -> bool:
  # CHECK THE CORRECTS OF THE ENTERED COORDINATES
  coordinates = str(f"{size_ship}{vertical_axis}{horizontal_axis}{orientation_ship}")
  if len(coordinates) == 4 or len(coordinates) == 5:
    if str(coordinates[0]).isdigit() == False or int(coordinates[0]) < 1 or int(coordinates[0]) > 4:
      if random:
        print("Bad SIZE SHIP! Integer between 1 and 4.")
      return True
    elif coordinates[1].isdigit() or list(X_AXIS.keys()).count(coordinates[1].upper()) != 1:
      if random:
        print("Bad HORIZONTAL! Letter between 'a' and 'j'.")
      return True
    elif list(X_AXIS.values()).count(int(coordinates[2:-1]) - 1) != 1 or int(coordinates[2:-1]) < 1 or int(coordinates[2:-1]) > 10:
      if random:
        print("Bad VERTICAL! Integer between 1 and 10.")
      return True
    elif coordinates[-1].isdigit() or coordinates[-1] != "h" and coordinates[-1] != "v":
      if random:
        print("Bad ORIENTATION! 'h' as horizontal and 'v' as vertical.")
      return True
    size_ship = int(coordinates[0])  # CYFRA OD 1 do 4
    horizontal_axis = int(coordinates[2:-1])  # CYFRA OD 1 do 10
    vertical_axis = X_AXIS[str(vertical_axis).upper()]  # CYFRA OD 0 do 9
    orientation_ship = str(coordinates[-1]).lower()  # LITERA h lub v
  else:
    return True
    # CHECK AREA IN AND AROUND FOR THE NEW SHIP
  # IN area, must be clear!
  for i in range(size_ship):
    if int(f"{horizontal_axis - 1}{vertical_axis}") + i < 0 or int(f"{horizontal_axis - 1}{vertical_axis}") + i > 99:
      if random:
        print("Area outside board!")
      return True
    elif board[int(f"{horizontal_axis - 1}{vertical_axis}") + i] != " ":
      if random:
        board_print()
        print("This area is occupied by another ship! Please correct the coordinates!")
      return True
      #  AROUND area, must be clear!
  around_area = (-11, -10, -9, -1, 1, 9, 10, 11)  # field around checking area, step by step
  for i in range(size_ship):
    for area in around_area:
      if orientation_ship == "h":
        check_area_h = int(f"{horizontal_axis - 1 + i}{vertical_axis}") + i + area
        if 0 <= check_area_h <= 99:
          if check_area_h in list(range(0, 100, 10)) or check_area_h in list(range(9, 100, 10)):
            continue
          if board[check_area_h] != " ":
            if random:
              board_print()
              print("Too close to another ship!")
            return True
      elif orientation_ship == "v":
        check_area_v = int(f"{horizontal_axis - 1 + i * 10}{vertical_axis}") + i + area
        if 0 <= check_area_v <= 99:
          if check_area_v in list(range(0, 100, 10)) or check_area_v in list(range(9, 100, 10)):
            continue
          if board[check_area_v] != " ":
            if random:
              board_print()
              print("Too close to another ship!")
            return True
  # PUT SHIP ON BOARD, CHECK IT FITS
  # horizontal
  if orientation_ship == "h" and int(f"{horizontal_axis - 1}{vertical_axis}") + (size_ship - 1) < int(
          f"{horizontal_axis}0"):
    for i in range(size_ship):
      board[int(f"{horizontal_axis - 1}{vertical_axis}") + i] = ships.ship[0 + i]
      # vertical
  elif orientation_ship == "v" and not (
          size_ship == 2 and horizontal_axis == 10 or size_ship == 3 and horizontal_axis >= 9 or size_ship == 4 and horizontal_axis >= 8):
    for i in range(size_ship):
      board[int(f"{horizontal_axis - 1}{vertical_axis}") + i * 10] = ships.ship[0 + i]
  else:
    if random:
      print("Please check coordinates!!")
    return True
  game_statistic[who]['parts_ships'] += size_ship


def fleet_player(*args):
  if game_statistic['player']['ships'] >= game_statistic['all_ships']:
    print("Fleet was led out to sea!")
    return False
  ships_number_on_fleet = 1
  while ships_number_on_fleet <= game_statistic["all_ships"]:
    if args == tuple("3", ) and ships_number_on_fleet <= game_statistic["all_ships"]:
      random_position = coordinate_random()
      if coordinate(random_position[0], random_position[2:-1], random_position[1], random_position[-1], board_player, False, "player"):
        continue
    else:
      while True:
        position = input(f"Coordinate Your {ships_number_on_fleet} ship: ")
        if len(position) < 4 or len(position) > 5:
          print("Coordinates for example: 1-4 SIZE SHIP, a-j HORIZONTAL AXIS, 1-10 VERTICAL AXIS, h-v ORIENTATION.)")
          continue
        else:
          break
      # position = "4d4h"
      if coordinate(position[0], position[2:-1], position[1], position[-1], board_player, True, "player"):
        continue
    game_statistic["player"]["ships"] += 1
    ships_number_on_fleet += 1
    if args != tuple("3", ):
      board_print()
  if ships_number_on_fleet > game_statistic["all_ships"]:
    clear_screen()
    # board_print()
    print("Your all fleet on the sea!, Start battle!")
    return True


def fleet_cpu(ships: int) -> None:
  global board_cpu, game_statistic
  if game_statistic['cpu']['ships'] >= game_statistic['all_ships']:
    return False
  ships_number_on_fleet = 1
  while ships_number_on_fleet <= ships:
    position = coordinate_random()
    if coordinate(position[0], position[2:-1], position[1], position[-1], board_cpu, False, "cpu"):  # plansza cpu widoczna dla gracza
      continue
    game_statistic["cpu"]["ships"] += 1
    ships_number_on_fleet += 1


def game_over(who: str) -> None:
  game_statistic['turns'] -= 1
  print(f"{game_statistic[who]['name']} WIN the BATTLE after {game_statistic['turns']} turns!")
  show_statistic()
  total_time_game()
  exit()


def reset_game():
  global board_player, board_cpu, board_cpu_hidden, game_statistic
  board_player = [" "] * 100
  board_cpu = [" "] * 100
  board_cpu_hidden = [" "] * 100
  game_statistic = {"all_ships": 4,
                    "player":
                      {"name": "Player", "ships": 0, "parts_ships": 0, "missed": 0, "hit": 0, "shots": 0},
                    "cpu":
                      {"name": "CPU", "ships": 0, "parts_ships": 0, "missed": 0, "hit": 0, "shots": 0},
                    "turns": 0
                    }


def battle(*args: bool) -> None:

  def shot(who: str, *args: bool) -> bool:  # jako wsad funkcja potrzebuje tylko strony strzelającej. "player" albo "cpu"
    shot = ""
    if who == "player":
      board = board_cpu
      while True:
        if args[0] == False:
          shot = input("Your shot!: ")
        else:
          shot = choice(ascii_lowercase[:10]) + str(randint(1, 10))
          # sleep(1)
        if shot == "ss":
          show_statistic()
          continue
        elif shot == "e":
          total_time_game()
          exit()
        try:
          coordinate_shot = int(f"{int(shot[1:]) - 1}{X_AXIS[shot[0].upper()]}")
          if board[coordinate_shot] == ships.missed or board[coordinate_shot] == ships.hit_at_sea or board[
            coordinate_shot] == ships.hit_sunk:
            print("You've already shot here! Please correct.")
            continue
        except:
          print('Bad coordinate!')
          continue
        break
    elif who == "cpu":
      board = board_player
      while True:
        shot = choice(ascii_lowercase[:10]) + str(randint(1, 10))
        coordinate_shot = int(f"{int(shot[1:]) - 1}{X_AXIS[shot[0].upper()]}")
        if board[coordinate_shot] == ships.missed or board[coordinate_shot] == ships.hit_at_sea or board[
          coordinate_shot] == ships.hit_sunk:
          continue
        break
    coordinate_shot = int(f"{int(shot[1:]) - 1}{X_AXIS[shot[0].upper()]}")
    if board[coordinate_shot] == ships.unknown_area:  # strzał niecelny
      board[coordinate_shot] = ships.missed
      print(f"{game_statistic[who]['name']} shot on {shot.capitalize()} -> Missed!")
      game_statistic[who]["missed"] += 1
      game_statistic[who]["shots"] += 1
      return False
    elif board[coordinate_shot] == ships.ship[0]:  # strzał celny
      board[coordinate_shot] = ships.hit_at_sea
      print(f"{game_statistic[who]['name']} shot on {shot.capitalize()} -> Hit!")
      game_statistic[who]["hit"] += 1
      game_statistic[who]["shots"] += 1
      return True

  while True:
    game_statistic['turns'] += 1
    # PLAYER shot
    if game_statistic['cpu']['parts_ships'] == 0:
      game_over("player")
    if shot("player", args[0]) == True:
      game_statistic['cpu']['parts_ships'] -= 1
      game_statistic['turns'] -= 1
      clear_screen()
      board_print()
      continue
    board_print()
    # CPU shot
    if game_statistic['player']['parts_ships'] == 0:
      game_over("cpu")
    if shot("cpu", args[0]) == True:
      game_statistic['player']['parts_ships'] -= 1
      clear_screen()
      board_print()
      continue
    board_print()


def menu() -> None:
  global board_player, board_cpu, board_cpu_hidden, game_statistic
  board_print()
  while True:
    choose = input(f"Choose menu option: ")
    if choose == "1":  # start battle
      if game_statistic['player']['parts_ships'] == 0 or game_statistic['cpu']['parts_ships'] == 0:
        print("Where is a fleet?")
      else:
        battle(False)
    elif choose == "2":  # player fleet
      fleet_player()
    elif choose == "3":  # random player fleet
      fleet_player(choose)
      fleet_cpu(game_statistic['all_ships'])
      board_print()
    elif choose == "4":  # clear board
      board_player = [" "] * 100
      game_statistic['player']['ships'] = 0
      board_print()
    elif choose == "5":  # show statistic
      show_statistic()
    elif choose == "6":  # setup game
      while True:
        print("Setup Game"
              "\n1 - Change Your name"
              "\n2 - Ships in fleet"
              "\n3 - Default settings"
              "\n4 - Exit to menu")
        setup_choose = input("Choose setup: ")
        if setup_choose == "1":
          game_statistic['player']['name'] = input("Enter name: ")
          print('Done!')
        elif setup_choose == "2":
          game_statistic['all_ships'] = int(input("How many ships in fleet?: "))
          print('Done!')
        elif setup_choose == "3":
          game_statistic['player']['name'] = "Player"
          game_statistic['all_ships'] = 4
          print("Done!")
        elif setup_choose == "4":
          menu()
    elif choose == "7":  # reset game
      reset_game()
      board_print()
    elif choose == "8":  # exit game
      total_time_game()
      exit()
    elif choose == "9":  # reset ustawień i gry, wygenerowanie losowej floty dla obu stron, toczenie losowej bitwy aż do zwycięstwa jednej ze stron z jednoczesną wizualizacją obu flot.
      reset_game()
      fleet_player("3")
      fleet_cpu(game_statistic['all_ships'])
      board_print()
      battle(True)
      show_statistic()
      total_time_game()
      exit()


clear_screen()
fleet_cpu(game_statistic['all_ships'])  # tworzenie floty dla CPU
menu()
total_time_game()
