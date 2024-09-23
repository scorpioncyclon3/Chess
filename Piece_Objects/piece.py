class Piece:
    #attributes
    player_white: bool
    value: int
    available_moves: set[tuple[int, int]]

    def __init__(self, player_white, value):
        self.player_white = player_white
        self.value = value
        self.available_moves = set()

    def get_player(self):
        return self.player_white

    def get_value(self):
        return self.value

    def get_available_moves(self):
        return self.available_moves

    def find_available_moves(self, board, x, y):
        self.available_moves = set()
