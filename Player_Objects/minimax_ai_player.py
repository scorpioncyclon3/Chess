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
        # player is already in checkmate
        if board.check_for_checkmate(self.get_player()):
            return board, True

        start_time = time.perf_counter()
        results = self.minimax_move_selection(
            board, 0, self.get_player()
        )
        board = deepcopy(results[2])
        end_time = time.perf_counter()
        print("Time taken:", end_time - start_time)
        return board
    
    def minimax_move_selection(
        self, board, current_recursion_depth, player
    ):
        # each item in evaluations will be a tuple structured as:
        # (evaluation score, neutral bonus incentive score, board state)
        evaluations = []
        for y in range(8):
            for x in range(8):
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
                        evaluations = self.minimamx_move(
                            evaluations, board, player, x, y,
                            move, current_recursion_depth
                        )
        return(self.pick_best_move(evaluations, board))

    def minimamx_move(
        self, evaluations, board, player, x, y, move, current_recursion_depth
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
            evaluations = self.minimax_leaf_node(evaluations, temp_copy, player)
        # if it is not a leaf node, continue recursing
        # then use the selected leaf node's value
        else:
            evaluations = self.minimax_branch_node(
                evaluations, board, temp_copy, player, current_recursion_depth
            )
        return(evaluations)

    def minimax_leaf_node(self, evaluations, temp_copy, player):
        evaluation = temp_copy.evaluate_state(player)
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
        return(evaluations)
    
    def minimax_branch_node(
        self, evaluations, board, temp_copy, player, current_recursion_depth
    ):
        # gets the best-case value
        leaf_val = self.minimax_move_selection(
            temp_copy,
            current_recursion_depth+1,
            not player
        )
        # error protection
        if leaf_val[0] != "Error":
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
        else:
            print("Child boards cause errors")
            board.print_state()
        return(evaluations)

    def pick_best_move(self, evaluations, board):
        # error protection
        if len(evaluations):
            # shuffles the list in case of a tie
            random.shuffle(evaluations)
            # finds the most effective move
            # picks the highest value
            evaluations.sort(
                reverse=True,
                key=lambda i: (i[0])
            )
            # returns the best item
            return evaluations[0]
        else:
            # returns an error, layer above should ignore this move
            print("No available moves in simulation")
            board.print_state()
            return(("Error", 0, board))
