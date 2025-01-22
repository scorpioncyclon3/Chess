from copy import deepcopy
import random
import time

from Player_Objects.player import Player

class Minimax_AI_Player(Player):
    player_white: bool
    max_recursion_depth: int

    def __init__(self, player_white, max_recursion_depth=1):
        Player.__init__(
            self,
            player_white
        )
        self.max_recursion_depth = max_recursion_depth

    def move(self, board):
        board = deepcopy(board)
        # checkmate
        if board.check_for_checkmate(self.get_player()):
            return board, True

        start_time = time.perf_counter()
        results = self.cool_temp_funct_name(
            board, 0, self.get_player()
        )
        board = deepcopy(results[1])
        end_time = time.perf_counter()
        print("Time taken:", end_time - start_time)
        return board, False
    
    def cool_temp_funct_name(
        self, board, current_recursion_depth, player
    ):
        evaluations = []

        for y in range(0,8):
            for x in range(0,8):
                # if the player's piece is in that coordinate
                if (
                    board.get_board()[y][x] != None
                    and board.get_board()[y][x].get_player()
                    == player
                ):
                    # simulates each of the moves for that piece
                    for move in (
                        board.get_board()[y][x].get_available_moves()
                    ):
                        # simulates the move
                        temp_copy = deepcopy(board)
                        temp_copy.move_piece(
                            old_x=x, old_y=y,
                            new_x=move[0], new_y=move[1],
                            real=False)
                        #temp_copy.print_state()
                        # check whether it is in checkmate only if it
                        # is already in check
                        white_king_in_check, black_king_in_check = (
                            temp_copy.check_for_check()
                        )
                        # if one player is in check, check whether it
                        # is a checkmate
                        if (
                            (white_king_in_check or black_king_in_check)
                            and temp_copy.check_for_checkmate(not player)
                        ):
                            if player:
                                evaluations.append(
                                    ((1, 0, 0, 0, 0), temp_copy)
                                )
                            else:
                                evaluations.append(
                                    ((-1, 0, 0, 0, 0), temp_copy)
                                )
                        # if it at a leaf node
                        elif (
                            current_recursion_depth
                            == self.max_recursion_depth
                        ):
                            evaluations.append(
                                (
                                    temp_copy.evaluate_state(real=False),
                                    temp_copy
                                )
                            )
                        # if it is not a leaf node, recurse again
                        else:
                            evaluations.append(
                                (
                                    self.cool_temp_funct_name(
                                        temp_copy,
                                        current_recursion_depth+1,
                                        (not player)
                                    )[0],
                                    temp_copy
                                )
                            )
        # removes all error-causing board states
        evaluations = list(filter(
            lambda i: (i[0] != "Error")
        ))
        # shuffles the list in case of a tie
        random.shuffle(evaluations)
        # finds the most effective move
        if player:
            evaluations = sorted(
                evaluations,
                reverse=True,
                key=lambda i: (i[0][0], i[0][1], i[0][3])
            )
        else:
            evaluations = sorted(
                evaluations,
                reverse=True,
                key=lambda i: (i[0][0]*-1, i[0][2], i[0][4])
            )

        # error protection
        if len(evaluations):
            # returns the best item
            return evaluations[0]
        else:
            # returns an error, layer above should ignore this move
            print("No available moves in simulation")
            board.print_state()
            return(("Error", board))
