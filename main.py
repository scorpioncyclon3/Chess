from board import Board
from Player_Objects.player import Player
from Player_Objects.manual_player import Manual_Player
from Player_Objects.minimax_ai_player import Minimax_AI_Player

board = Board()
player_1 = Manual_Player(player_white=True)
player_2 = Manual_Player(player_white=False)
#player_1 = Minimax_AI_Player(player_white=True, max_recursion_depth=2)
#player_2 = Minimax_AI_Player(player_white=False, max_recursion_depth=2)
player_1_turn = True

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
        game_running = False
