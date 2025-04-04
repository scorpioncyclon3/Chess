from Player_Objects.minimax_ai_player import *

class Alpha_Beta_AI_Player(Minimax_AI_Player):
    player_white: bool
    max_recursion_depth: int
    #αβ

    def __init__(self, player_white, max_recursion_depth=1):
        Minimax_AI_Player.__init__(
            self,
            player_white,
            max_recursion_depth
        )
    
    def minimax_move_selection(
        self, board, current_recursion_depth, player,
        alpha=-2147483647, beta=2147483647
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
                            move, current_recursion_depth,
                            alpha, beta
                        )
                        # alpha beta pruning
                        # if the score is greater than alpha, change alpha to be the score
                        if evaluations and evaluations[-1][0] > alpha:
                            alpha = evaluations[-1][0]
                        # cut off condition
                        if alpha >= beta:
                            return(("Prune", 0, board))
        return(self.pick_best_move(evaluations, board))

    def minimamx_move(
        self, evaluations, board, player, x, y, move, current_recursion_depth,
        alpha, beta
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
                evaluations, board, temp_copy, player, current_recursion_depth,
                alpha, beta
            )
        return(evaluations)

    
    def minimax_branch_node(
        self, evaluations, board, temp_copy, player, current_recursion_depth,
        alpha, beta
    ):
        # gets the best-case value
        leaf_val = self.minimax_move_selection(
            temp_copy,
            current_recursion_depth+1,
            not player,
            # swaps alpha and beta values
            beta * -1,
            alpha * -1
        )
        # ignores pruned nodes & error protection
        if leaf_val[0] != "Prune" and leaf_val[0] != "Error":
            # inverts the evaluation score
            # plus double the neutral incentives to account for the *-1
            inverted_val = (leaf_val[0] * -1) + (2 * leaf_val[1])
            # adds it to evaluations after inverting the score
            evaluations.append(
                (
                    # the highest guaranteed leaf node score
                    inverted_val,
                    # the neutral bonus incentive score
                    leaf_val[1],
                    # the board state
                    temp_copy
                )
            )
        # if child nodes are error-causing, print current state for debugging
        # TODO resolve errors
        #elif leaf_val[0] == "Error":
            #print("Child boards cause errors")
            #board.print_state()
        return(evaluations)

    def pick_best_move(self, evaluations, board):
        # error protection
        if len(evaluations):
            # filters out pruned states
            evaluations = list(filter(
                lambda i: (i[0] != "Pruned"),
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
            # returns the best item
            return evaluations[0]
        else:
            # returns an error, layer above should ignore this move
            # TODO resolve errors
            #print("No available moves in simulation")
            #board.print_state()
            return(("Error", 0, board))
