from copy import deepcopy

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
    all_available_moves_white: set()
    all_available_moves_black: set()

    def __init__(self):
        # create board
        self.board = []
        for i in range(0,8):
            self.board.append([])
            for j in range(0,8):
                self.board[-1].append(None)

        # tracks the total value on the board
        self.total_white_value, self.total_black_value = 0, 0
        # tracks the available moves at a given point
        self.all_available_moves_white = set()
        self.all_available_moves_black = set()

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
        self.all_available_moves_white = set()
        self.all_available_moves_black = set()
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
                        self.all_available_moves_white.update(
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
                        self.all_available_moves_black.update(
                            self.get_board()[y][x].get_available_moves()
                        )
                        # if the piece is a king, track its position
                        if str(type(self.get_board()[y][x])) == (
                            "<class 'Piece_Objects.king.King'>"
                        ):
                            black_king_pos = (x,y)
        # finds out whether either kings can be taken by a piece of
        # the opposite colour
        return(
            (white_king_pos in self.all_available_moves_black),
            (black_king_pos in self.all_available_moves_white)
        )

    def remove_illegal_moves_from_set(
        self, available_moves, player, x, y
    ):
        # removes illegal moves
        to_remove = set()
        for move in available_moves:
            # copies the self to simulate moves with
            board_copy = deepcopy(self)
            # simulates the move in the copy
            board_copy.move_piece(
                old_x=x, old_y=y,
                new_x=move[0], new_y=move[1],
                real=False
            )
            # checks whether it moves self into check
            white_king_in_check, black_king_in_check = board_copy.check_for_check()
            # if it moves the player into check
            if (player and white_king_in_check) or (not player and black_king_in_check):
                # tracks the illegality of the move
                to_remove.add((move[0],move[1]))
        # removes the illegal moves
        for move in to_remove:
            available_moves.remove(move)
        return available_moves

    def check_for_checkmate(self, player):
        # tracks the true set of available moves
        true_available_moves_player = set()
        # loops through each piece
        for y in range(0,8):
            for x in range(0,8):
                # piece in location
                if self.get_board()[y][x] != None:
                    # gets the true set of available moves for that piece
                    try:
                        true_available_moves_piece = (
                            self.remove_illegal_moves_from_set(
                                self.get_board()[y][x].get_available_moves(),
                                player,
                                x, y
                        ))
                    except:
                        print("Error in checking piece", x, y)
                        true_available_moves_piece = set()
                    # if the piece belongs to the player being checked
                    if player == self.get_board()[y][x].get_player():
                        true_available_moves_player = (
                            true_available_moves_player.union(
                                true_available_moves_piece
                        ))
        print(true_available_moves_player)
        return(len(true_available_moves_player) == 0)

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

        # determines the total value of board control
        white_board_control_value = 0
        black_board_control_value = 0
        #self.all_available_moves_white
        #self.all_available_moves_black
