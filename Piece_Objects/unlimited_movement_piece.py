from Piece_Objects.piece import Piece

"""
Pieces that can move an unlimited distance (Rooks, Bishops, and Queens).
The get_directions() function should return a tuple specific to the piece-type
containing tuples of x and y coordinates, starting north and rotating clockwise.
"""

class Unlimited_Movement_Piece(Piece):
    # piece attributes
    player_white: bool
    value: int
    available_moves: set[tuple[int, int]]

    def __init__(self, player_white, value):
        Piece.__init__(self, player_white, value)

    @staticmethod
    def get_directions():
        return(())

    def find_available_moves(self, board, x, y):
        self.available_moves = set()
        for direction in self.get_directions():
            self.find_available_moves_in_direction(board, x, y, direction)

    def find_available_moves_in_direction(self, board, x, y, direction):
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
                if board.get_board()[checking_y][checking_x] is not None:
                    # piece of opposite team
                    if (
                        board.get_board()[checking_y][checking_x].get_player()
                        != self.get_player()
                    ):
                        self.available_moves.add((checking_x, checking_y))
                    # stop checking this direction
                    end_reached = True
                # checking empty position
                else:
                    self.available_moves.add((checking_x, checking_y))

    def refresh_direction(self, board, x, y, direction):
        # removes every move in the direction being refreshed
        to_remove = set()
        for move in self.get_available_moves():
            # finds the difference between the move and the current location
            difference = (
                move[0]-x,
                move[1]-y
            )
            # check if the signs match
            # if both directions are positive when multiplied together, 
            # the signs must match between the direction and the difference
            if difference[0]*direction[0] >= 0 and difference[1]*direction[1] >= 0:
                # check if the zeroes are correct (if present)
                if direction[0] == 0:
                    if difference[0] != 0:
                        # skip if the zero is incorrect
                        continue
                if direction[1] == 0:
                    if difference[1] != 0:
                        # skip if the zero is incorrect
                        continue
                # if the direction is diagonal (neither directions are 0),
                # check if the absolute values both equal 1
                # (since the signs are already proven to be correct)
                if direction[0] != 0 and direction[1] != 0:
                    if (
                        difference[0]*direction[0]
                        == difference[1]*direction[1]
                        == 1
                    ):
                        # skip if the absolute values aren't both 1
                        continue
                to_remove.add(move)

        self.available_moves.difference_update(to_remove)
        self.find_available_moves_in_direction(board, x, y, direction)
