from Piece_Objects.piece import Piece

"""
Pieces that can move an unlimited distance (Rooks, Bishops, and Queens).
The directions tuple should contain tuples of x and y coordinates,
starting north and rotating clockwise.
"""

class Unlimited_Movement_Piece(Piece):
    # piece attributes
    player_white: bool
    value: int
    available_moves: set[tuple[int, int]]
    # unique attributes
    direction = tuple[tuple[int, int]]

    def __init__(self, player_white, value, directions):
        Piece.__init__(self, player_white, value)
        self.directions = directions

    def find_available_moves(self, board, x, y):
        self.available_moves = set()
        for direction in self.directions:
            checking_x = x
            checking_y = y
            end_reached = False
            while not end_reached:
                # checks the next position
                checking_x += direction[0]
                checking_y += direction[1]
                # if at the board boundaries, stop checking this direction
                if not 0 <= checking_x <= 7 or not 0 <= checking_y <= 7:
                    end_reached = True

                if not end_reached:
                    # piece in position being checked
                    if board.get_board()[checking_y][checking_x] != None:
                        # piece of opposite team
                        if board.get_board()[checking_y][checking_x].get_player() != self.get_player():
                            self.available_moves.add((checking_x, checking_y))
                        # stop checking this direction
                        end_reached = True
                    # checking empty position
                    else:
                        self.available_moves.add((checking_x, checking_y))
