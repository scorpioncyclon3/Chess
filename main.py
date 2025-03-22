from Player_Objects.player import Player
from Player_Objects.manual_player import Manual_Player
from Player_Objects.minimax_ai_player import Minimax_AI_Player
from play import play_game

single_game = False
#single_game = True

# plays a single game for testing purposes or for fun
if single_game:
    p1, p2 = 0, 0
    match p1:
        case 0:
            player_1 = Manual_Player(player_white=True)
        case 1:
            player_1 = Minimax_AI_Player(player_white=True, max_recursion_depth=2)
        case _:
            player_1 = Manual_Player(player_white=True)
    match p2:
        case 0:
            player_2 = Manual_Player(player_white=False)
        case 1:
            player_2 = Minimax_AI_Player(player_white=False, max_recursion_depth=2)
        case _:
            player_1 = Manual_Player(player_white=True)
    play_game(player_1, player_2)

# automated data collection
else:
    for trial in range(0,5):
        for depth in range(3,4):
            player_1 = Minimax_AI_Player(
                player_white=True, 
                max_recursion_depth=depth,
            )
            player_2 = Minimax_AI_Player(
                player_white=False,
                max_recursion_depth=depth, 
            )
            play_game(
                player_1,
                player_2,
                data_collection=True,
                trial_name="mm-" + str(depth) + "-" + str(trial)
            )

            """
            player_1 = Alpha_Beta_AI_Player(
                player_white=True,
                max_recursion_depth=depth,
            )
            player_2 = Alpha_Beta_AI_Player(
                player_white=False,
                max_recursion_depth=depth,
            )
            play_game(
                player_1,
                player_2,
                data_collection=True,
                trial_name="αβ-" + str(depth) + "-" + str(trial)
            )
            """
