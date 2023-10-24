import dominoes
import random as rand


from dominoes.players import *
from dominoes.q_learner import QLearner

#%% helper functions. should refactor

def simple_state(game):
    if len(game.board) == 0:
        return [None, None, game.turn, game.hands]
    
    return [game.board.left_end(), game.board.right_end(), game.turn, game.hands]
    
#%% 
def train(players, n=100, tiles_per_hand = 7, verbose=False):
        """
        TODO: write docstring
        """

        for i in range(n):

            if verbose is True:
                print(f"Playing training game {i + 1}")

            # initialize a new game
            game = dominoes.Game.new(tiles_per_hand= tiles_per_hand)
            # Keep track of last move made by each of the four players; initialization
            last = {
                0: {"state": None, "action": None},
                1: {"state": None, "action": None},
                2: {"state": None, "action": None},
                3: {"state": None, "action": None},
            }

            # play the game until completion
            while game.result is None:
                # get current state
                
                state = simple_state(game).copy()
                current_player = players[game.turn]

                # choose an action to take based on the current state
                action = current_player(game)
                # Keep track of last state and action
                last[game.turn]["state"] = state
                last[game.turn]["action"] = action

                # unpack action to make move
                move_tile, side = action
                game.make_move(move_tile, side)

                # get the new state
                new_state = simple_state(game).copy()

                # When game is over, update Q values with rewards
                if game.result is not None:

                    if verbose is True:
                        print(f"Final Board: {game.board}. Game over. {game.result.points} points.")
                    # points signals the winning team; if 0 and 2 win, points is positive
                    # if 1 and 3 win, points is negative
                    #points = game.result.points
                    reward = 1 if game.result.points > 0 else -1 # alternate reward function
                    # if the winning team is 0 and 2, reward is 1

                    # update Q values for each of the 4 players
                    for player_num in range(4):
                        if player_num == 0 or player_num == 2:
                            current_player.update(
                                last[player_num]["state"],
                                last[player_num]["action"],
                                new_state,
                                reward
                            )
                        else:
                            current_player.update(
                                last[player_num]["state"],
                                last[player_num]["action"],
                                new_state,
                                -reward
                            )
                    break

                # If game is continuing, no rewards yet for any of the players
                # elif last[game.turn]["state"] is not None:
                #     current_player.update(
                #         last[game.turn]["state"],
                #         last[game.turn]["action"],
                #         new_state,
                #         0
                #     )
        print("Done training")
        


# %%
#