from Piece_Objects.unlimited_movement_piece import Unlimited_Movement_Piece

"""
Moves horizontally or vertically an unlimited distance.
"""

class Rook(Unlimited_Movement_Piece):
    # piece attributes
    player_white: bool
    value: int
    available_moves: set[tuple[int, int]]
    # unlimited movement piece attributes
    direction = tuple[tuple[int, int]]

    def __init__(self, player_white):
        Unlimited_Movement_Piece.__init__(
            self,
            player_white,
            value=5,
            directions=((0,-1), (1,0), (0,1), (-1,0))
        )
