from Piece_Objects.limited_movement_piece import Limited_Movement_Piece

"""
Can move one space in any direction.
"""

class King(Limited_Movement_Piece):
    # piece attributes
    player_white: bool
    value: int
    available_moves: set[tuple[int, int]]
    # unique attributes
    can_castle: bool

    def __init__(self, player_white):
        Limited_Movement_Piece.__init__(
            self,
            player_white,
            value=2147483647
        )
        self.can_castle = True

    @staticmethod
    def get_directions():
        return((0,-1), (1,-1), (1,0), (1,1), (0,1), (-1,1), (-1,0), (-1,-1))

    def find_available_moves_in_direction(self, board, x, y, direction):
        # calls parent function
        Limited_Movement_Piece.find_available_moves_in_direction(
            self, board, x, y, direction
        )
        # checks for castling availability
        # if the direction is horizontal
        if direction[1] == 0:
            # if self hasn't moved
            if self.get_can_castle():
                # white player
                if self.get_player():
                    row = 7
                # black player
                else:
                    row = 0
                # direction is left, left rook hasn't moved,
                # and the spaces between are empty
                if (
                    (direction[0] == -1)
                    and str(type(board.get_board()[row][0])) == (
                        "<class 'Piece_Objects.rook.Rook'>")
                    and board.get_board()[row][0].get_can_castle()
                    and (
                        board.get_board()[row][1]
                        is board.get_board()[row][2]
                        is board.get_board()[row][3]
                        is None
                    )
                ):
                    self.available_moves.add((2, row))
                # direction is right, right rook hasn't moved,
                # and the spaces between are empty
                if (
                    (direction[0] == 1)
                    and str(type(board.get_board()[row][7])) == (
                        "<class 'Piece_Objects.rook.Rook'>")
                    and board.get_board()[row][7].get_can_castle()
                    and (
                        board.get_board()[row][6]
                        is board.get_board()[row][5]
                        is None
                    )
                ):
                    self.available_moves.add((6, row))

    def refresh_direction(self, board, x, y, direction):
        # removes every move in the direction being refreshed
        if (x+direction[0], y+direction[1]) in self.get_available_moves():
            self.available_moves.remove((x+direction[0], y+direction[1]))
        # removes castling moves in the direction being refreshed
        if (x+(direction[0]*2), y+direction[1]) in self.get_available_moves():
            self.available_moves.remove((x+(direction[0]*2), y+direction[1]))
        self.find_available_moves_in_direction(board, x, y, direction)

    def get_can_castle(self):
        return self.can_castle

    def prevent_castling(self):
        self.can_castle = False
