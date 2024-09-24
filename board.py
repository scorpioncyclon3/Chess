from Piece_Objects.bishop import Bishop
from Piece_Objects.king import King
from Piece_Objects.knight import Knight
from Piece_Objects.pawn import Pawn
from Piece_Objects.queen import Queen
from Piece_Objects.rook import Rook

class Board:
    board: list[list[object]]

    def __init__(self):
        # create board
        self.board = []
        for i in range(0,8):
            self.board.append([])
            for j in range(0,8):
                self.board[-1].append(None)

        # fill board
        for (player_colour, y) in ((True, 7), (False, 0)):
            self.add_piece(King(player_white=player_colour), 4, y)
            self.add_piece(Queen(player_white=player_colour), 3, y)
            self.add_piece(Rook(player_white=player_colour), 0, y)
            self.add_piece(Rook(player_white=player_colour), 7, y)
            self.add_piece(Bishop(player_white=player_colour), 2, y)
            self.add_piece(Bishop(player_white=player_colour), 5, y)
            self.add_piece(Knight(player_white=player_colour), 1, y)
            self.add_piece(Knight(player_white=player_colour), 6, y)
        for (player_colour, y) in ((True, 6), (False, 1)):
            for x in range(0,8):
                self.add_piece(Pawn(player_white=player_colour), x, y)

    def get_board(self):
        return self.board

    def print_state(self):
        print('Board:')
        print("   AA BB CC DD EE FF GG HH")
        # loops through each row
        for y in range(0,8):
            # tracks the row as a string
            row_str = " "+str(8-y)
            # loops through
            for x in range(0,8):
                # adds spaces between characters
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
                        # king
                        case "<class 'Piece_Objects.king.King'>":
                            row_str += "K"
                        # queen
                        case "<class 'Piece_Objects.queen.Queen'>":
                            row_str += "Q"
                        # rook
                        case "<class 'Piece_Objects.rook.Rook'>":
                            row_str += "R"
                        # bishop
                        case "<class 'Piece_Objects.bishop.Bishop'>":
                            row_str += "B"
                        # knight
                        case "<class 'Piece_Objects.knight.Knight'>":
                            row_str += "N"
                        # pawn
                        case "<class 'Piece_Objects.pawn.Pawn'>":
                            row_str += "P"
            print(row_str)
        print("")

    def add_piece(self, piece, x, y):
        self.board[y][x] = piece

    def move_piece(self, old_x, old_y, new_x, new_y):
        # moves the piece
        self.board[new_y][new_x] = self.board[old_y][old_x]
        # removes the old piece
        self.board[old_y][old_x] = None

        # castling
        if str(type(self.get_board()[new_y][new_x])) == "<class 'Piece_Objects.king.King'>":
            self.board[new_y][new_x].prevent_castling()
            # castle left
            if old_x - new_x == 2:
                self.board[new_y][3] = self.board[new_y][0]
                self.board[new_y][0] = None
            # castle right
            elif old_x - new_x == -2:
                self.board[new_y][5] = self.board[new_y][7]
                self.board[new_y][7] = None
        elif str(type(self.get_board()[new_y][new_x])) == "<class 'Piece_Objects.rook.Rook'>":
            self.board[new_y][new_x].prevent_castling()
        # pawn double movement
        elif str(type(self.get_board()[new_y][new_x])) == "<class 'Piece_Objects.pawn.Pawn'>":
            self.board[new_y][new_x].prevent_double_move()
