from board import Board
from player import Player

board = Board()
player_1 = Player(player_white=True, type="manual")
player_2 = Player(player_white=False, type="manual")
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
        checkmate = player_1.get_move_selection(board)
    else:
        print("Black turn.")
        checkmate = player_2.get_move_selection(board)
    player_1_turn = not player_1_turn
    print(checkmate)
    if checkmate:
        print("Checkmate.")
        print(("White" if player_1_turn else "Black") + " wins.")
        game_running = False
