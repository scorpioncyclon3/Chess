from Piece_Objects.bishop import Bishop
from Piece_Objects.king import King
from Piece_Objects.knight import Knight
from Piece_Objects.pawn import Pawn
from Piece_Objects.queen import Queen
from Piece_Objects.rook import Rook

class Board:
    board: list[list[object]]
    total_white_value: int
    total_black_value: int

    def __init__(self):
        # create board
        self.board = []
        for i in range(0,8):
            self.board.append([])
            for j in range(0,8):
                self.board[-1].append(None)

        # tracks the total value on the board
        self.total_white_value, self.total_black_value = 0, 0

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
                pass#self.add_piece(Pawn(player_white=player_colour), x, y)
        

    def get_board(self):
        return self.board

    def print_state(self):
        print('Board:')
        print("   AA BB CC DD EE FF GG HH")
        # loops through each row
        for y in range(0,8):
            # tracks the row as a string
            row_str = "0"+str(8-y)
            # loops through
            for x in range(0,8):
                # adds spaces between characters
                row_str += " "

                # empty space
                if str(type(self.board[y][x])) == "<class 'NoneType'>":
                    row_str += "--"
                else:
                    # adds the piece colour
                    row_str += (
                        "W" if self.board[y][x].player_white else "B"
                    )

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

    def add_piece(self, piece:object, x:int, y:int):
        # adds the piece value to the total if it isn't a king
        if str(type(piece)) != "<class 'Piece_Objects.king.King'>":
            if piece.player_white:
                self.total_white_value += piece.value
            else:
                self.total_black_value += piece.value
        # adds the piece
        self.board[y][x] = piece

    def move_piece(
        self, old_x:int, old_y:int, new_x:int, new_y:int, real:bool
    ):
        # if taking a piece
        if self.board[new_y][new_x] != None:
            # adds the value of it t the total
            if self.board[new_y][new_x].get_player():
                self.total_white_value -= (
                    self.board[new_y][new_x].get_value()
                )
                if real:
                    print("Total white value remaining ",
                        self.total_white_value)
            else:
                self.total_black_value -= (
                    self.board[new_y][new_x].get_value()
                )
                if real:
                    print("Total black value remaining ",
                        self.total_black_value)

        # moves the piece
        self.board[new_y][new_x] = self.board[old_y][old_x]
        # removes the old piece
        self.board[old_y][old_x] = None

        # castling
        if str(type(self.get_board()[new_y][new_x])) == (
            "<class 'Piece_Objects.king.King'>"
        ):
            self.board[new_y][new_x].prevent_castling()
            # castle left
            if old_x - new_x == 2:
                self.board[new_y][3] = self.board[new_y][0]
                self.board[new_y][0] = None
            # castle right
            elif old_x - new_x == -2:
                self.board[new_y][5] = self.board[new_y][7]
                self.board[new_y][7] = None
        elif str(type(self.get_board()[new_y][new_x])) == (
            "<class 'Piece_Objects.rook.Rook'>"
        ):
            self.board[new_y][new_x].prevent_castling()
        # pawn double movement
        elif str(type(self.get_board()[new_y][new_x])) == (
            "<class 'Piece_Objects.pawn.Pawn'>"
        ):
            self.board[new_y][new_x].prevent_double_move()
        self.evaluate_state(real)

    def check_for_check(self):
        # finds whether either player is currently in Check
        all_available_moves_white = set()
        all_available_moves_black = set()
        #loops through all positions
        for y in range(0,8):
            for x in range(0,8):
                # if the space is not empty, add its available moves to
                # all_available_moves
                if str(type(self.get_board()[y][x])) != "<class 'NoneType'>":
                    # updates the piece's available_moves set
                    self.get_board()[y][x].find_available_moves(self, x, y)
                    if self.get_board()[y][x].player_white:
                        # adds the items from the piece's available_moves set
                        # to the all_available_moves_white set
                        all_available_moves_white.update(
                            self.get_board()[y][x].get_available_moves()
                        )
                        # if the piece is a king, track its position
                        if str(type(self.get_board()[y][x])) == (
                            "<class 'Piece_Objects.king.King'>"
                        ):
                            white_king_pos = (x,y)
                    else:
                        # adds the items from the piece's available_moves set
                        # to the all_available_moves_black set
                        all_available_moves_black.update(
                            self.get_board()[y][x].get_available_moves()
                        )
                        # if the piece is a king, track its position
                        if str(type(self.get_board()[y][x])) == (
                            "<class 'Piece_Objects.king.King'>"
                        ):
                            black_king_pos = (x,y)
        # finds out whether either kings can be taken by a piece of the
        # opposite colour
        white_king_in_check, black_king_in_check = False, False
        if white_king_pos in all_available_moves_black:
            white_king_in_check = True
        if black_king_pos in all_available_moves_white:
            black_king_in_check = True
        return(white_king_in_check, black_king_in_check)

    def evaluate_state(self, real:bool):
        # evaluates the overall state of the board for both players

        # to account for trading being favourable when up material but
        # adverse when down material, remaining value is evaluated as a ratio

        # converts ratio from opposing_piece_value : piece_value
        # to 1 : adjusted_piece_value, where a high adjusted_piece_value
        # is favourable
        white_adjusted_piece_value = (
            self.total_black_value / self.total_white_value)
        black_adjusted_piece_value = (
            self.total_white_value / self.total_black_value)
        if real:
            print("White adjusted piece value ", white_adjusted_piece_value)
            print("Black adjusted piece value ", black_adjusted_piece_value)
