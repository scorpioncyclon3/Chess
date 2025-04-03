from Player_Objects.player import Player
from Player_Objects.manual_player import Manual_Player
from Player_Objects.minimax_ai_player import Minimax_AI_Player
from Player_Objects.αβ_ai_player import Alpha_Beta_AI_Player
from play import play_game
from create_data_directory import create_data_directory

single_game = False
#single_game = True

# plays a single game for testing purposes or for fun
if single_game:
    p1, p2 = 2, 2
    match p1:
        case 0:
            player_1 = Manual_Player(player_white=True)
        case 1:
            player_1 = Minimax_AI_Player(player_white=True, max_recursion_depth=2)
        case 2:
            player_1 = Alpha_Beta_AI_Player(player_white=True, max_recursion_depth=2)
        case _:
            player_1 = Manual_Player(player_white=True)
    match p2:
        case 0:
            player_2 = Manual_Player(player_white=False)
        case 1:
            player_2 = Minimax_AI_Player(player_white=False, max_recursion_depth=2)
        case 2:
            player_2 = Alpha_Beta_AI_Player(player_white=False, max_recursion_depth=2)
        case _:
            player_1 = Manual_Player(player_white=True)
    play_game(player_1, player_2)

# automated data collection
else:
    # creates a new "experiment" with a folder to store its data
    experiment_num = create_data_directory()

    for trial in range(0,5):
        for depth in range(1,4):
            for player_type in ("mm", "αβ"):
                match player_type:
                    case "mm":
                        player_1 = Minimax_AI_Player(
                            player_white=True, 
                            max_recursion_depth=depth,
                        )
                        player_2 = Minimax_AI_Player(
                            player_white=False,
                            max_recursion_depth=depth, 
                        )
                    case "αβ":
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
                    trial_name=(
                        "Data/"
                        + str(experiment_num)
                        + "/"
                        + "-".join((
                            str(experiment_num),
                            str(player_type),
                            str(depth),
                            str(trial)
                        ))
                        + ".txt"
                    )
                )
