from Player_Objects.player import Player
from Player_Objects.manual_player import Manual_Player
from Player_Objects.minimax_ai_player import Minimax_AI_Player
from play_game import play_game

player_1 = Manual_Player(player_white=True)
player_2 = Manual_Player(player_white=False)
player_1 = Minimax_AI_Player(player_white=True, max_recursion_depth=2)
player_2 = Minimax_AI_Player(player_white=False, max_recursion_depth=2)

play_game(player_1, player_2)
