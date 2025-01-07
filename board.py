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
        mode = "text"
        mode = "icon"
        print('Board:')
        if mode == "text": print("   AA BB CC DD EE FF GG HH")
        elif mode == "icon": print("  A B C D E F G H")
        # loops through each row
        for y in range(0,8):
            # tracks the row as a string
            if mode == "text": row_str = "0"+str(8-y)
            elif mode == "icon": row_str = str(8-y)
            # loops through
            for x in range(0,8):
                # adds spaces between characters
                row_str += " "

                # empty space
                if str(type(self.board[y][x])) == "<class 'NoneType'>":
                    if mode == "text": row_str += "--"
                    elif mode == "icon": row_str += "-"
                else:
                    # adds the piece colour
                    if self.board[y][x].player_white:
                        if mode == "text": piece_str = "W"
                        elif mode == "icon": piece_str = 9811
                    else:
                        if mode== "text": piece_str = "B"
                        elif mode == "icon": piece_str = 9817

                    # adds a different character for each piece type
                    match str(type(self.board[y][x])):
                        # king
                        case "<class 'Piece_Objects.king.King'>":
                            match mode:
                                case "text": piece_str += "K"
                                case "icon": piece_str += 1
                        # queen
                        case "<class 'Piece_Objects.queen.Queen'>":
                            match mode:
                                case "text": piece_str += "Q"
                                case "icon": piece_str += 2
                        # rook
                        case "<class 'Piece_Objects.rook.Rook'>":
                            match mode:
                                case "text": piece_str += "R"
                                case "icon": piece_str += 3
                        # bishop
                        case "<class 'Piece_Objects.bishop.Bishop'>":
                            match mode:
                                case "text": piece_str += "B"
                                case "icon": piece_str += 4
                        # knight
                        case "<class 'Piece_Objects.knight.Knight'>":
                            match mode:
                                case "text": piece_str += "N"
                                case "icon": piece_str += 5
                        # pawn
                        case "<class 'Piece_Objects.pawn.Pawn'>":
                            match mode:
                                case "text": piece_str += "P"
                                case "icon": piece_str += 6
                    # if in icon mode, convert from int to unicode char
                    if mode == "icon": piece_str = chr(piece_str)
                    row_str += piece_str
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
        
        # refreshes the available moves of potentially impacted pieces
        self.refresh_affected_pieces(old_x, old_y)
        self.refresh_affected_pieces(new_x, new_y)

    def refresh_affected_pieces(self, x, y):
        # refreshes the available moves set for any pieces that could be
        # affected by a specific move

        # refreshes moves in a star pattern (accounts for every potentially
        # piece except for knights)
        for direction in (
            (0,-1), (1,-1), (1,0), (1,1), (0,1), (-1,1), (-1,0), (-1,-1)
        ):
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
                    if self.get_board()[checking_y][checking_x] is not None:
                        piece = self.get_board()[checking_y][checking_x]
                        # refreshes pieces that could be affected
                        if isinstance(piece, (Queen, Rook, Bishop)):
                            # if the target piece can move in the direction of
                            # the currently moving piece
                            if direction in piece.get_directions():
                                # refreshes the available_moves set in the
                                # direction of the currently moving piece
                                piece.refresh_direction(
                                    self, checking_x*-1, checking_y*-1)
                        elif isinstance(piece, King):
                            # if the king is within a tile of the moving piece
                            if (
                                (1 >= x-checking_x >= -1)
                                and (1 >= y-checking_y >= -1)
                            ):
                                piece.refresh_direction(
                                    self, checking_x*-1, checking_y*-1)
                        elif isinstance(piece, Pawn):
                            pass
                            # TODO
                        # stop checking this direction
                        end_reached = True

        # refreshes potential knight moves

    def check_for_check(self):
        # finds whether either player is currently in Check
        self.all_available_moves_white = set()
        self.all_available_moves_black = set()
        #loops through all positions
        for y in range(0,8):
            for x in range(0,8):
                # if the space is not empty, add its available moves
                # to all_available_moves
                if (
                    str(type(self.get_board()[y][x]))
                    != "<class 'NoneType'>"
                ):
                    # updates the piece's available_moves set
                    self.get_board()[y][x].find_available_moves(
                        self, x, y
                    )
                    if self.get_board()[y][x].player_white:
                        # adds the moves from the piece's set
                        # to the all_available_moves_white set
                        self.all_available_moves_white.update(
                            (self.get_board()[y][x]
                                .get_available_moves()
                            )
                        )
                        # if the piece is a king, track its position
                        if str(type(self.get_board()[y][x])) == (
                            "<class 'Piece_Objects.king.King'>"
                        ):
                            white_king_pos = (x,y)
                    else:
                        # adds the moves from the piece's set
                        # to the all_available_moves_black set
                        self.all_available_moves_black.update(
                            (self.get_board()[y][x]
                                .get_available_moves()
                            )
                        )
                        # if the piece is a king, track its position
                        if str(type(self.get_board()[y][x])) == (
                            "<class 'Piece_Objects.king.King'>"
                        ):
                            black_king_pos = (x,y)

        # finds out whether either kings can currently be taken by
        # a piece of the opposite colour
        # if an error occurs, their king has been taken during a
        # checkmate simulation
        try:
            white_in_check = (
                white_king_pos in self.all_available_moves_black
            )
        except:
            white_in_check = True
        try:
            black_in_check = (
                white_king_pos in self.all_available_moves_white
            )
        except:
            black_in_check = True
        
        return(white_in_check, black_in_check)

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
            white_king_in_check, black_king_in_check = (
                board_copy.check_for_check()
            )
            # if it moves the player into check
            if (
                (player and white_king_in_check)
                or (not player and black_king_in_check)
            ):
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
                    # gets the true set of available moves for it
                    try:
                        true_available_moves_piece = (
                            self.remove_illegal_moves_from_set(
                                (self.get_board()[y][x]
                                    .get_available_moves()
                                ),
                                player,
                                x, y
                        ))
                    except:
                        print("Error in checking piece", x, y)
                        true_available_moves_piece = set()
                        self.print_state()
                        # crashes self so that error-causing board states can be identified
                        {0:0}[1]
                    # if the piece belongs to the player being checked
                    if player == self.get_board()[y][x].get_player():
                        true_available_moves_player = (
                            true_available_moves_player.union(
                                true_available_moves_piece
                        ))
        return(len(true_available_moves_player) == 0)

    def evaluate_state(self, real:bool):
        # evaluates the overall state of the board for both players

        # to account for trading being favourable when up material
        # but adverse when down material, remaining value is
        # evaluated as a ratio

        # converts ratio from piece_value : opposing_piece_value
        # to adjusted_piece_value : 1, where a high
        # adjusted_piece_value is favourable
        white_adjusted_piece_value = (
            self.total_white_value / self.total_black_value)
        black_adjusted_piece_value = (
            self.total_black_value / self.total_white_value)
        if real:
            print(
                "White adjusted piece value ",
                white_adjusted_piece_value
            )
            print(
                "Black adjusted piece value ",
                black_adjusted_piece_value
            )

        # determines the total value of board control
        white_board_control_value = 0
        black_board_control_value = 0
        #self.all_available_moves_white
        #self.all_available_moves_black
        return (
            0,
            white_adjusted_piece_value,
            black_adjusted_piece_value,
            white_board_control_value,
            black_board_control_value
        )
