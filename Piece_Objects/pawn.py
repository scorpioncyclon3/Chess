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
    can_double_move: bool

    def __init__(self, player_white):
        Piece.__init__(
            self,
            player_white,
            value=1,
        )
        self.can_double_move = True

    def get_directions(self):
        return ((0, -1) if self.get_player() else (0, 1))

    def find_available_moves(self, board, x, y):
        self.available_moves = set()
        # only takes the vertical direction
        direction = self.get_directions()[1]
        # prevents the pawn from moving off the board
        if 0 <= y+direction <= 7:
            # movement forwards
            if board.get_board()[y+direction][x] is None:
                self.available_moves.add((x, y+direction))
                # double movement forwards
                if (self.get_can_double_move()
                    and board.get_board()[y+(direction*2)][x] is None
                ):
                    self.available_moves.add((x, y+(direction*2)))
            # piece diagonally left and piece owned by opponent
            if (
                x > 0 and board.get_board()[y+direction][x-1] is not None
                and board.get_board()[y+direction][x-1].get_player()
                != self.get_player()
            ):
                self.available_moves.add((x-1, y+direction))
            # piece diagonally right and piece owned by opponent
            if (
                x < 7 and board.get_board()[y+direction][x+1] is not None
                and board.get_board()[y+direction][x+1].get_player()
                != self.get_player()
            ):
                self.available_moves.add((x+1, y+direction))
            # TODO en passant

    def get_can_double_move(self):
        return self.can_double_move

    def prevent_double_move(self):
        self.can_double_move = False
