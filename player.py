from board import Board

class Player:
    player_white: bool
    type: str

    def __init__(self, player_white, type):
        self.player_white = player_white
        self.type = type

    def get_player(self):
        return player_white

    def get_move_selection(self, board):
        match self.type:
            case "manual":
                return self.manual_move(board, self.player_white)

    def manual_move(self, board, player_white):
        selected_coords = ()
        available_moves = set()
        piece_selection_ongoing = True
        while piece_selection_ongoing:
            # TODO idiot proof the inputs
            valid = False
            while not valid:
                location = input("Coordinate: ")
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
                board.move_piece(selected_coords[0], selected_coords[1], x, y)
                # exit piece selection
                piece_selection_ongoing = False
            # if the piece at the selected coordinate is owned by the player
            elif board.get_board()[y][x] != None and board.get_board()[y][x].get_player() == player_white:
                # select the piece
                selected_coords = (x,y)
                selected_piece = board.get_board()[y][x]
                selected_piece.find_available_moves(board, x, y)
                available_moves = selected_piece.get_available_moves()
            # illegal choice
            else:
                print("Illegal.")
        print()
        return board
