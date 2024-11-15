from board import Board
from Player_Objects.player import Player
from Player_Objects.manual_player import Manual_Player

board = Board()
player_1 = Manual_Player(player_white=True)
player_2 = Manual_Player(player_white=False)
player_1_turn = True

game_running = True
while game_running:
    board.print_state()
    # one side in check
    white_king_in_check, black_king_in_check = board.check_for_check()
    if white_king_in_check:
        print("White king in check.")
    if black_king_in_check:
        print("Black king in check.")

    if player_1_turn:
        print("White turn.")
        board, checkmate = player_1.move(board)
    else:
        print("Black turn.")
        board, checkmate = player_2.move(board)
    player_1_turn = not player_1_turn
    print(checkmate)
    if checkmate:
        print("Checkmate.")
        print(("White" if player_1_turn else "Black") + " wins.")
        game_running = False
