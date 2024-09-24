from Piece_Objects.piece import Piece

"""
Moves horizontally or vertically an unlimited distance.
"""

class Pawn(Piece):
    # piece attributes
    player_white: bool
    value: int
    available_moves: set[tuple[int, int]]
    # unique attributes
    can_double_move = True

    def __init__(self, player_white):
        Piece.__init__(
            self,
            player_white,
            value=1,
        )
        self.can_double_move = True

    def find_available_moves(self, board, x, y):
        self.available_moves = set()
        if self.get_player():
            direction = -1
        else:
            direction = 1
        # movement forwards
        if board.get_board()[y+direction][x] == None:
            self.available_moves.add((y+direction, x))
            # double movement forwards
            if self.get_can_double_move() and board.get_board()[y+(direction*2)][x] == None:
                self.available_moves.add((y+(direction*2), x))
        # piece diagonally left
        if x > 0 and board.get_board()[y+direction][x-1] != None:
            self.available_moves.add((y+direction, x-1))
        # piece diagonally right
        if x < 7 and board.get_board()[y+direction][x+1] != None:
            self.available_moves.add((y+direction, x+1))

    def get_can_double_move(self):
        return self.can_double_move

    def prevent_double_move(self):
        self.can_double_move = False
