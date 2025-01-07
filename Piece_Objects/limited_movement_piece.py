from Piece_Objects.piece import Piece

"""
Pieces that can move a limited distance (Kings, Knights).
The get_directions() function should return a tuple specific to the piece-type
containing tuples of x and y coordinates, starting north and rotating clockwise.
"""

class Limited_Movement_Piece(Piece):
    # piece attributes
    player_white: bool
    value: int
    available_moves: set[tuple[int, int]]

    def __init__(self, player_white, value, directions):
        Piece.__init__(self, player_white, value)

    def get_directions(self):
        return(())

    def find_available_moves(self, board, x, y):
        self.available_moves = set()
        for direction in self.get_directions():
            checking_x = x + direction[0]
            checking_y = y + direction[1]
            # if inside the board
            if 0 <= checking_x <= 7 and 0 <= checking_y <= 7:
                # piece in position being checked
                if board.get_board()[checking_y][checking_x] != None:
                    # piece of opposite team
                    if board.get_board()[checking_y][checking_x].get_player() != self.get_player():
                        self.available_moves.add((checking_x, checking_y))
                # checking empty position
                else:
                    self.available_moves.add((checking_x, checking_y))
