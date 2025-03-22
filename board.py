from copy import deepcopy

from Piece_Objects.bishop import Bishop
from Piece_Objects.king import King
from Piece_Objects.knight import Knight
from Piece_Objects.pawn import Pawn
from Piece_Objects.queen import Queen
from Piece_Objects.rook import Rook

class Board:
    board: list[list[object]]
    total_white_piece_value: int
    total_black_piece_value: int
    all_available_moves_white: set[tuple[int, int]]
    all_available_moves_black: set[tuple[int, int]]

    def __init__(self):
        # create board
        self.board = []
        for i in range(8):
            self.board.append([])
            for j in range(8):
                self.board[-1].append(None)

        # tracks the total value on the board
        self.total_white_piece_value, self.total_black_piece_value = 0, 0
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
            for x in range(8):
                self.add_piece(Pawn(player_white=player_colour), x, y)
        # TEST
        # gives the white player a loaded shotgun aimed directly at the black
        # king to test whether the AI is smart enough to pull the trigger
        #self.add_piece(Rook(True), 3, 1)
        #self.add_piece(Rook(True), 3, 2)

        # loops through all positions to find the available moves for all pieces
        for y in range(8):# TODO change to "range(8)"
            for x in range(8):
                # if the space is not empty, fill its available moves set
                if self.get_board()[y][x] is not None:
                    # updates the piece's available_moves set
                    self.get_board()[y][x].find_available_moves(
                        self, x, y
                    )

    def get_board(self):
        return self.board

    def print_state(self):
        print(self.board_to_string())

    def board_to_string(self):
        mode = "text"
        mode = "icon"
        print('Board:')
        if mode == "text": print("   AA BB CC DD EE FF GG HH")
        elif mode == "icon": print("  A B C D E F G H")
        board_str = ""
        # loops through each row
        for y in range(8):
            # tracks the row as a string
            if mode == "text": board_str += "0"+str(8-y)
            elif mode == "icon": board_str += str(8-y)
            # loops through
            for x in range(8):
                # adds spaces between characters
                board_str += " "

                # empty space
                if self.board[y][x] is None:
                    if mode == "text": board_str += "--"
                    elif mode == "icon": board_str += "-"
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
                    board_str += piece_str
            board_str += "\n"
        return board_str

    def add_piece(self, piece:object, x:int, y:int):
        # adds the piece value to the total if it isn't a king
        if not isinstance(piece, King):
            if piece.player_white:
                self.total_white_piece_value += piece.value
            else:
                self.total_black_piece_value += piece.value
        # adds the piece
        self.board[y][x] = piece

    def move_piece(
        self, old_x:int, old_y:int, new_x:int, new_y:int, real:bool
    ):
        # if taking a piece
        if self.board[new_y][new_x] != None:
            # adds the value of it to the total
            if self.board[new_y][new_x].get_player():
                self.total_white_piece_value -= (
                    self.board[new_y][new_x].get_value()
                )
                if real:
                    print("Total white value remaining ",
                        self.total_white_piece_value)
            else:
                self.total_black_piece_value -= (
                    self.board[new_y][new_x].get_value()
                )
                if real:
                    print("Total black value remaining ",
                        self.total_black_piece_value)

        # moves the piece
        self.board[new_y][new_x] = self.board[old_y][old_x]
        # removes the old piece
        self.board[old_y][old_x] = None
        # resets the piece's available_moves set
        self.board[new_y][new_x].find_available_moves(self, new_x, new_y)

        # edge case movements
        # castling
        if isinstance(self.get_board()[new_y][new_x], King):
            self.board[new_y][new_x].prevent_castling()
            # castle left
            if old_x - new_x == 2:
                # moves rook
                self.board[new_y][3] = self.board[new_y][0]
                self.board[new_y][0] = None
            # castle right
            elif old_x - new_x == -2:
                # moves rook
                self.board[new_y][5] = self.board[new_y][7]
                self.board[new_y][7] = None
        elif isinstance(self.get_board()[new_y][new_x], Rook):
            self.board[new_y][new_x].prevent_castling()
        # pawn double movement & promotion
        elif isinstance(self.get_board()[new_y][new_x], Pawn):
            self.board[new_y][new_x].prevent_double_move()
            # if a white pawn reaches the top row
            if self.board[new_y][new_x].get_player() and new_y == 0:
                # removes the pawn's value from white player's total
                self.total_white_piece_value -= 1
                # adds a white queen in it's place
                self.add_piece(Queen(True), new_x, new_y)
                self.board[new_y][new_x].find_available_moves(self, new_x, new_y)
            # if a black pawn reaches the bottom row
            if not self.board[new_y][new_x].get_player() and new_y == 7:# TODO fix
                # removes the pawn's value from black player's total
                self.total_black_piece_value -= 1
                # adds a black queen in it's place
                self.add_piece(Queen(False), new_x, new_y)
                self.board[new_y][new_x].find_available_moves(self, new_x, new_y)
        
        # refreshes the available moves of potentially impacted pieces
        self.refresh_affected_pieces(old_x, old_y)
        self.refresh_affected_pieces(new_x, new_y)

    def refresh_affected_pieces(self, x, y):
        # refreshes the available moves set for any pieces that could be
        # affected by a specific move

        # refreshes moves in a star pattern (accounts for every potentially
        # piece except for knights)
        for direction in Queen.get_directions():
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
                                    self,
                                    checking_x,
                                    checking_y,
                                    (direction[0]*-1, direction[1]*-1)
                                )
                        elif isinstance(piece, King):
                            # if the king is within a tile of the moving piece
                            if (
                                (1 >= x-checking_x >= -1)
                                and (1 >= y-checking_y >= -1)
                            ):
                                piece.refresh_direction(
                                    self,
                                    checking_x,
                                    checking_y,
                                    (direction[0]*-1, direction[1]*-1)
                                )
                        elif isinstance(piece, Pawn):
                            # if the pawn is in range and moving in the
                            # correct direciton
                            if ((
                                # if it is a white pawn, only reset the
                                # available_moves set if the moving piece is
                                # in the same row, one greater, or two greater
                                piece.get_player() and (
                                    checking_y == y
                                    or checking_y == y+1
                                    or checking_y == y+2
                                )
                            ) or (
                                # if it is a black pawn, only reset the
                                # available_moves set if the moving piece is
                                # in the same row, one lesser, or two lesser
                                not piece.get_player() and (
                                    checking_y == y
                                    or checking_y == y-1
                                    or checking_y == y-2
                                )
                            )):
                                piece.find_available_moves(
                                    self, checking_x, checking_y
                                )
                        # stop checking this direction
                        end_reached = True

        # refreshes potential knight moves
        for direction in Knight.get_directions():
            checking_x = x + direction[0]
            checking_y = y + direction[1]
            # if inside the board
            if 0 <= checking_x <= 7 and 0 <= checking_y <= 7:
                piece = self.get_board()[checking_y][checking_x]
                # knight in position being checked
                if isinstance(piece, Knight):
                    piece.refresh_direction(
                        self,
                        checking_x,
                        checking_y,
                        (direction[0]*-1, direction[1]*-1)
                    )

    def check_for_check(self):
        # finds whether either player is currently in Check
        self.all_available_moves_white = set()
        self.all_available_moves_black = set()
        #loops through all positions
        for y in range(8):
            for x in range(8):
                # if the space is not empty, add its available moves
                # to all_available_moves
                if self.get_board()[y][x] is not None:
                    piece = self.get_board()[y][x]
                    if piece.player_white:
                        # adds all of the moves from the piece's set
                        # to the board's all_available_moves_white set
                        self.all_available_moves_white.update(
                            piece.get_available_moves()
                        )
                        # if the piece is a king, track its position
                        if isinstance(piece, King):
                            white_king_pos = (x,y)
                    else:
                        # adds all of the moves from the piece's set
                        # to the board's all_available_moves_black set
                        self.all_available_moves_black.update(
                            piece.get_available_moves()
                        )
                        # if the piece is a king, track its position
                        if isinstance(piece, King):
                            black_king_pos = (x,y)
        # finds out whether either kings can currently be taken by
        # a piece of the opposite colour
        # if an error occurs, their king has been taken during a
        # checkmate simulation, which is essentially equivalent to a check for
        # the purpose of determining a checkmate
        try:
            white_in_check = white_king_pos in self.all_available_moves_black
        except:
            white_in_check = True
        try:
            black_in_check = black_king_pos in self.all_available_moves_white
        except:
            black_in_check = True
        return(white_in_check, black_in_check)

    def remove_illegal_moves_from_piece_set(self, x, y):
        # removes illegal moves from a piece's set
        available_moves = self.get_board()[y][x].get_available_moves()
        piece_player = self.get_board()[y][x].get_player()
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
                (piece_player and white_king_in_check)
                or (not piece_player and black_king_in_check)
            ):
                # tracks the illegality of the move
                to_remove.add((move[0],move[1]))
        # removes the illegal moves
        for move in to_remove:
            available_moves.remove(move)
        # DEBUG
        #if len(available_moves): print(f"({x}, {y}) legal moves: {available_moves}")
        #else: print(f"No legal moves for ({x}, {y})")
        return available_moves

    def check_for_checkmate(self, player):
        # tracks the true set of available moves
        true_available_moves_player = set()
        # loops through each piece
        for y in range(8):
            for x in range(8):
                # piece owned by the player being checked in location
                if (
                    self.get_board()[y][x] is not None
                    and player == self.get_board()[y][x].get_player()
                ):
                    # gets the true set of available moves for it
                    try:
                        true_available_moves_player.update(
                            self.remove_illegal_moves_from_piece_set(x, y)
                        )
                    except:
                        print("Error in checking piece", x, y)
                        self.print_state()
                        # crashes self so that error-causing board states can
                        # be identified and fixed
                        {0:0}[1]
        # DEBUG
        #print(f"All legal moves for player {player}: {true_available_moves_player}")
        # returns False if the set is empty, since empty sets evaluate to False
        # and filled sets are True
        return(not true_available_moves_player)

    # TODO add stalemates

    def evaluate_state(self, player_white, real:bool=False):
        # evaluates the overall state of the board for the focused player

        # can only be called on non-checkmate nodes, so checkmate can be ignored
        """
        # to account for trading being relatively equal for both players,
        # but slightly favourable when up material and slightly adverse when
        # down material, remaining piece value is evaluated as a ratio

        # converts ratio from piece_value : opposing_piece_value
        # to adjusted_piece_value : 10, where a high
        # adjusted_piece_value is favourable
        if player_white:
            adjusted_piece_value = (
                10 * self.total_white_piece_value / self.total_black_piece_value
            )
            if real:
                print(
                    "White adjusted piece value ",
                    adjusted_piece_value
                )
        else:
            adjusted_piece_value = (
                -10 * self.total_black_piece_value / self.total_white_piece_value
            )
            if real:
                print(
                    "Black adjusted piece value ",
                    adjusted_piece_value
                )
        """
        # evaluates the total piece value of the player
        if player_white:
            adjusted_piece_value = 10 * (
                self.total_white_piece_value - self.total_black_piece_value
            )
        else:
            adjusted_piece_value = 10 * (
                self.total_black_piece_value - self.total_white_piece_value
            )

        # adds a bonus for checking the opponent and a penalty for being in check
        check_bonus_value = 0
        white_king_in_check, black_king_in_check = (
            self.check_for_check()
        )
        if (
            (player_white and black_king_in_check)
            or (not player_white and white_king_in_check)
        ):
            check_bonus_value += 25
        if (
            (player_white and white_king_in_check)
            or (not player_white and black_king_in_check)
        ):
            check_bonus_value -= 25

        # determines the total value of board control
        white_board_control_value = 0
        black_board_control_value = -0
        # since check_for_check was recently called, all_available_moves_white
        # and all_available_moves_black are up to date
        
        # weights central tiles to be more important
        value_dict = {
            0:1.0,
            1:1.2,
            2:1.4,
            3:1.5,
            4:1.5,
            5:1.4,
            6:1.2,
            7:1.0
        }
        for move in self.all_available_moves_white:
            white_board_control_value += (
                1
                * value_dict[move[0]]
                * value_dict[move[1]]
            )
        for move in self.all_available_moves_black:
            black_board_control_value += (
                1
                * value_dict[move[0]]
                * value_dict[move[1]]
            )
        if player_white:
            adjusted_board_value = (white_board_control_value
                - black_board_control_value)
        else:
            adjusted_board_value = (black_board_control_value
                - white_board_control_value)

        # incentivises trades to progress the game faster
        # will be worth at most 16, which is just over one and a half pawns
        anti_coward_bonus_value = (
            80 - self.total_white_piece_value - self.total_black_piece_value
        ) / 5

        return (
            (adjusted_piece_value
            + adjusted_board_value
            + check_bonus_value,
            anti_coward_bonus_value)
        )
