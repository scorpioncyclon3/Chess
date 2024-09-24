from Piece_Objects.limited_movement_piece import Limited_Movement_Piece

"""
Can move one space in any direction.
"""

class King(Limited_Movement_Piece):
    # piece attributes
    player_white: bool
    value: int
    available_moves: set[tuple[int, int]]
    # limited movement piece attributes
    direction = tuple[tuple[int, int]]
    # unique attributes
    can_castle = True

    def __init__(self, player_white):
        Limited_Movement_Piece.__init__(
            self,
            player_white,
            value=2147483647,
            directions=((0,-1), (1,-1), (1,0), (1,1), (0,1), (-1,1), (-1,0), (-1,-1))
        )
        self.can_castle = True

    def find_available_moves(self, board, x, y):
        Limited_Movement_Piece.find_available_moves(self, board, x, y)
        # if self hasn't moved
        if self.get_can_castle():
            # white player
            if self.get_player():
                row = 7
            # black player
            else:
                row = 0
            # left rook hasn't moved
            if board.get_board()[row][0] != None and board.get_board()[row][0].get_can_castle():
                # if the spaces are empty
                if board.get_board()[row][1] == board.get_board()[row][2] == board.get_board()[row][3] == None:
                    self.available_moves.add((2, row))
            # right rook hasn't moved
            if board.get_board()[row][7] != None and board.get_board()[row][7].get_can_castle():
                # if the spaces are empty
                if board.get_board()[row][6] == board.get_board()[row][5] == None:
                    self.available_moves.add((6, row))


    def get_can_castle(self):
        return self.can_castle

    def prevent_castling(self):
        self.can_castle = False
