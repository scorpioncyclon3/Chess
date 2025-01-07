from Piece_Objects.limited_movement_piece import Limited_Movement_Piece

"""
Moves in an L shape (2 spaces one direction, one sidways).
"""

class Knight(Limited_Movement_Piece):
    # piece attributes
    player_white: bool
    value: int
    available_moves: set[tuple[int, int]]

    def __init__(self, player_white):
        Limited_Movement_Piece.__init__(
            self,
            player_white,
            value=3
        )

    def get_directions(self):
        return((1,-2), (2,-1), (2,1), (1,2), (-1,2), (-2,1), (-2,-1), (-1,-2))
