from board import Board

class Player:
    player_white: bool

    def __init__(self, player_white):
        self.player_white = player_white

    def get_player(self):
        return self.player_white
