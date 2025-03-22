import time

from board import Board
from Player_Objects.player import Player
from Player_Objects.manual_player import Manual_Player
from Player_Objects.minimax_ai_player import Minimax_AI_Player

def play_game(
    player_1: Player,
    player_2: Player,
    data_collection: bool = False,
    trial_name: str = ""
):
    # setup
    player_1_turn = True
    board = Board()
    turn = 0
    total_turn_time = 0.0
    game_running = True

    # creates a file for data collection
    if data_collection:
        f = open(trial_name, "a")

    while game_running:
        board.print_state()

        # check notification
        white_king_in_check, black_king_in_check = board.check_for_check()
        if white_king_in_check:
            print("White king in check.")
        if black_king_in_check:
            print("Black king in check.")

        # player turns
        start_time = time.perf_counter()
        if player_1_turn:
            print("White turn.")
            board = player_1.move(board)
        else:
            print("Black turn.")
            board = player_2.move(board)
        end_time = time.perf_counter()
        turn_time = end_time - start_time
        print(f"Time taken for turn #{turn}: {turn_time}")
        total_turn_time += turn_time

        # records the turn if it is a real trial
        if data_collection:
            f.write(f"Turn #{str(turn)}\n")
            f.write(f"Time - {str(total_turn_time)}\n")
            f.write(board.board_to_string() + "\n")

        # switches turn
        player_1_turn = not player_1_turn

        # increments the turn counter
        turn += 1
        
        checkmate = board.check_for_checkmate(player_1_turn)
        if checkmate:
            print("Checkmate.")
            print(("Black" if player_1_turn else "White") + " wins.")
            print("Final state:")
            board.print_state()
            game_running = False

        # imposes a turn limit for data collection games
        if data_collection and turn >= 50:
            game_running = False

    # averages the turn times
    if data_collection:
        average_turn_time = total_turn_time / turn
        f.write("\n\n\n")
        f.write("Total Time - ", total_turn_time)
        f.write("Turns - ", turn)
        f.write("Average Time - ", average_turn_time)
        f.close()
