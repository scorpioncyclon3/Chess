from Player_Objects.player import Player

class Manual_Player(Player):
    player_white: bool

    def __init__(self, player_white):
        Player.__init__(
            self,
            player_white
        )

    def move(self, board):
        selected_coords = ()
        available_moves = set()
        piece_selection_ongoing = True
        while piece_selection_ongoing:
            valid = False
            while not valid:
                location = input("Coordinate: ").upper()
                try:
                    x = {
                        "A":0,"B":1,"C":2,"D":3,"E":4,"F":5,"G":6,"H":7
                    }[location[0]]
                    y = {
                        "8":0,"7":1,"6":2,"5":3,"4":4,"3":5,"2":6,"1":7
                    }[location[1]]
                    valid = True
                except:
                    print("Invalid Input.")

            # if the move is available
            if (x,y) in available_moves:
                # move the piece
                board.move_piece(
                    old_x=selected_coords[0], old_y=selected_coords[1],
                    new_x=x, new_y=y, real=True
                )
                # exit piece selection
                piece_selection_ongoing = False

            # if the player owns the piece at the selected coordinate
            elif (
                board.get_board()[y][x] != None
                and board.get_board()[y][x].get_player()
                == self.player_white
            ):
                # select the piece
                selected_coords = (x,y)
                selected_piece = board.get_board()[y][x]
                selected_piece.find_available_moves(board, x, y)
                available_moves = selected_piece.get_available_moves()
                available_moves = board.remove_illegal_moves_from_piece_set(x, y)

            # illegal choice
            else:
                print("Illegal.")
        print()
        return board
