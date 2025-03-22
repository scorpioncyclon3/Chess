from board import Board
from Player_Objects.player import Player
from Player_Objects.manual_player import Manual_Player
from Player_Objects.minimax_ai_player import Minimax_AI_Player

def play_game(player_1: Player, player_2: Player):
    player_1_turn = True
    board = Board()
    game_running = True
    while game_running:
        board.print_state()

        #  checkmate notification
        white_king_in_check, black_king_in_check = board.check_for_check()
        if white_king_in_check:
            print("White king in check.")
        if black_king_in_check:
            print("Black king in check.")

        # player turns
        if player_1_turn:
            print("White turn.")
            board = player_1.move(board)
        else:
            print("Black turn.")
            board = player_2.move(board)

        # switches turn
        player_1_turn = not player_1_turn
        
        checkmate = board.check_for_checkmate(player_1_turn)
        if checkmate:
            print("Checkmate.")
            print(("Black" if player_1_turn else "White") + " wins.")
            print("Final state:")
            board.print_state()
            game_running = False
