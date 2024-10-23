from copy import deepcopy
from board import Board

class Player:
    player_white: bool
    type: str

    def __init__(self, player_white, type):
        self.player_white = player_white
        self.type = type

    def get_player(self):
        return self.player_white

    def get_move_selection(self, board):
        match self.type:
            case "manual":
                return self.manual_move(board, self.player_white)

    def remove_illegal_options(self, board, available_moves, x, y):
        # removes illegal moves
        to_remove = set()
        for move in available_moves:
            print(move)
            # copies the board
            board_copy = deepcopy(board)
            # simulates the move in the copy
            board_copy.move_piece(
                old_x=x, old_y=y, new_x=move[0], new_y=move[1], real=False
            )
            # checks whether it moves self into check
            white_king_in_check, black_king_in_check = board_copy.check_for_check()
            # if it moves self into check
            if (self.get_player() and white_king_in_check) or (not self.get_player() and black_king_in_check):
                # tracks the illegality of the move
                to_remove.add((move[0],move[1]))
        # removes the illegal moves
        for move in to_remove:
            available_moves.remove(move)
        return available_moves

    def manual_move(self, board, player_white):
        selected_coords = ()
        available_moves = set()
        piece_selection_ongoing = True
        while piece_selection_ongoing:
            valid = False
            while not valid:
                location = input("Coordinate: ").upper()
                try:
                    x = {
                        "A":0,"B":1,"C":2,"D":3,"E":4,"F":5,"G":6,"H":7
                    }[location[0]]
                    y = {
                        "8":0,"7":1,"6":2,"5":3,"4":4,"3":5,"2":6,"1":7
                    }[location[1]]
                    valid = True
                except:
                    print("Invalid Input.")

            # if the move is available
            if (x,y) in available_moves:
                # move the piece
                board.move_piece(
                    old_x=selected_coords[0], old_y=selected_coords[1], new_x=x, new_y=y, real=True
                )
                # exit piece selection
                piece_selection_ongoing = False

            # if the piece at the selected coordinate is owned by the player
            elif board.get_board()[y][x] != None and board.get_board()[y][x].get_player() == player_white:
                # select the piece
                selected_coords = (x,y)
                selected_piece = board.get_board()[y][x]
                selected_piece.find_available_moves(board, x, y)
                available_moves = selected_piece.get_available_moves()
                available_moves = self.remove_illegal_options(board, available_moves, x, y)

            # illegal choice
            else:
                print("Illegal.")
        print()
        return board
