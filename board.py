from Piece_Objects.rook import Rook
from Piece_Objects.bishop import Bishop
from Piece_Objects.queen import Queen
from Piece_Objects.king import King
from Piece_Objects.knight import Knight

class Board:
    board: list[list[object]]

    def __init__(self):
        self.board = []
        for i in range(0,8):
            self.board.append([])
            for j in range(0,8):
                self.board[-1].append(None)

        self.add_piece(Rook(player_white=False), 0, 0)
        self.add_piece(Rook(player_white=False), 7, 0)
        self.add_piece(Rook(player_white=True), 0, 7)
        self.add_piece(Rook(player_white=True), 7, 7)
        self.add_piece(Bishop(player_white=False), 2, 0)
        self.add_piece(Bishop(player_white=False), 5, 0)
        self.add_piece(Bishop(player_white=True), 2, 7)
        self.add_piece(Bishop(player_white=True), 5, 7)
        self.add_piece(Queen(player_white=False), 3, 0)
        self.add_piece(Queen(player_white=True), 3, 7)
        self.add_piece(King(player_white=False), 4, 0)
        self.add_piece(King(player_white=True), 4, 7)
        self.add_piece(Knight(player_white=False), 1, 0)
        self.add_piece(Knight(player_white=False), 6, 0)
        self.add_piece(Knight(player_white=True), 1, 7)
        self.add_piece(Knight(player_white=True), 6, 7)

    def get_board(self):
        return self.board

    def print_state(self):
        print('Board:')
        # loops through each row
        for y in range(0,8):
            # tracks the row as a string
            row_str = ""
            # loops through
            for x in range(0,8):
                # adds spaces between characters
                if row_str:
                    row_str += " "

                # for debugging
                #print(str(type(self.board[y][x])))

                
                # empty space
                if str(type(self.board[y][x])) == "<class 'NoneType'>":
                    row_str += "--"
                else:
                    # adds the piece colour
                    row_str += ("W" if self.board[y][x].player_white else "B")

                    # adds a different character for each piece type
                    match str(type(self.board[y][x])):
                        # rook
                        case "<class 'Piece_Objects.rook.Rook'>":
                            row_str += "R"
                        # bishop
                        case "<class 'Piece_Objects.bishop.Bishop'>":
                            row_str += "B"
                        # queen
                        case "<class 'Piece_Objects.queen.Queen'>":
                            row_str += "Q"
                        # king
                        case "<class 'Piece_Objects.king.King'>":
                            row_str += "K"
                        # knight
                        case "<class 'Piece_Objects.knight.Knight'>":
                            row_str += "N"
            print(row_str)
        print("")

    def add_piece(self, piece, x, y):
        self.board[y][x] = piece

    def move_piece(self, current_x, current_y, new_x, new_y):
        # moves the piece
        self.board[new_y][new_x] = self.board[current_y][current_x]
        # removes the old piece
        self.board[current_y][current_x] = None
