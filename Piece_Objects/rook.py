from Piece_Objects.unlimited_movement_piece import Unlimited_Movement_Piece

"""
Moves horizontally or vertically an unlimited distance.
"""

class Rook(Unlimited_Movement_Piece):
    # piece attributes
    player_white: bool
    value: int
    available_moves: set[tuple[int, int]]
    # unique attributes
    can_castle: bool

    def __init__(self, player_white):
        Unlimited_Movement_Piece.__init__(
            self,
            player_white,
            value=5
        )
        self.can_castle = True

    @staticmethod
    def get_directions():
        return((0,-1), (1,0), (0,1), (-1,0))

    def get_can_castle(self):
        return self.can_castle

    def prevent_castling(self):
        self.can_castle = False
