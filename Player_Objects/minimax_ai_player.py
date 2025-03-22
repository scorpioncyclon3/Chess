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
        results = self.really_cool_not_so_temporary_function_name(
            board, 0, self.get_player()
        )
        board = deepcopy(results[2])
        end_time = time.perf_counter()
        print("Time taken:", end_time - start_time)
        return board
    
    def really_cool_not_so_temporary_function_name(
        self, board, current_recursion_depth, player
    ):
        evaluations = []
        # each item in evaluations will be a tuple structured as:
        # (evaluation score, neutral bonus incentive score, board state)

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
                            evaluations.append(
                                (2147483647, 0, temp_copy)
                            )
                        # if it at a leaf node
                        elif (
                            current_recursion_depth
                            == self.max_recursion_depth
                        ):
                            evaluation = temp_copy.evaluate_state(
                                self.player_white
                            )
                            evaluations.append(
                                # (
                                # evaluation score,
                                # neutral bonus incentive score,
                                # board state
                                # )
                                (
                                    evaluation[0]+evaluation[1],
                                    evaluation[1],
                                    temp_copy
                                )
                            )
                        # if it is not a leaf node, continue recursing
                        # then use the selected leaf node's value
                        else:
                            # gets the best-case value
                            leaf_val = self.really_cool_not_so_temporary_function_name(
                                temp_copy,
                                current_recursion_depth+1,
                                not player
                            )
                            # adds it to evaluations after inverting the score
                            evaluations.append(
                                (
                                    # the highest guaranteed leaf node score
                                    leaf_val[0]
                                    # multiplied by negative 1
                                    * -1
                                    # plus double the neutral incentives
                                    # to account for the *-1
                                    + 2 * leaf_val[1],
                                    # the neutral bonus incentive score
                                    leaf_val[1],
                                    # the board state
                                    temp_copy
                                )
                            )
        # if child nodes are error-causing, print current state for debugging
        if len(evaluations) != len(
            list(filter(
                lambda i: (i[0] != "Error"),
                evaluations
            ))
        ):
            board.print_state()
        # removes all error-causing board states
        evaluations = list(filter(
            lambda i: (i[0] != "Error"),
            evaluations
        ))
        # shuffles the list in case of a tie
        random.shuffle(evaluations)
        # finds the most effective move
        # picks the highest value
        evaluations.sort(
            reverse=True,
            key=lambda i: (i[0])
        )

        # error protection
        if len(evaluations):
            # returns the best item
            return evaluations[0]
        else:
            # returns an error, layer above should ignore this move
            print("No available moves in simulation")
            board.print_state()
            return(("Error", 0, board))
