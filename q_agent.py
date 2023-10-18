"""
this script contains my first attempt at a q-learning agent. The state of the board is extremely simplified;
we only consider the edges of the board, and the tiles in the player's hand. 

Missing features:
    - Integration with the dominoes_lib package. I can use the players.py file as inspiration

Current state of the code:
    - The agent can play against itself, and learn from it (4 'agents' simultaneously)

examples of representation:
    - action = (tile, left = True/False) , as dictated by the library I have
    - simple_state = (left_end, right_end, player_in_turn, all hands)
    - state_edges = (left_end, right_end)
"""

import math
import random
import dominoes_lib as dominoes
import copy
#%% helper functions: should probably be part of library ( and not here)

def simple_state(game):
    return [game.board.left_end(), game.board.right_end(), game.turn, game.hands]

def state_edges(state):
    """
    returns the edges of the board as a tuple.
    """
    # TO-DO: re-organize so that there is no need to have "two states".
    # this is a hacky solution to the problem, but not ideal for debugging.
    return (state[0], state[1])

def available_actions(state):
    """
    Important function! should implement as method.
    uses game state to return list of available actions for the current
    player
    """
    left, right, turn, hands = state
    actions = set()
    for domino in hands[turn]:
        if left in domino:
            actions.add((domino, True))
        if right in domino:
            actions.add((domino, False))
    return actions


#%% Q-learning agent
class QAgent:
    '''
        Initialize AI with an empty Q-learning dictionary,
        an alpha (learning) rate, and an epsilon rate.

        The Q-learning dictionary maps `(state, action)`
        pairs to a Q-value (a number).
         - `state` is a tuple of the tiles at the edge of the board, e.g. (1,4)
         - `action` is a tuple `(tile, side)` for an action
    '''
    def __init__(self, alpha = 0.5, epsilon = 0.1):
        self.q = dict()
        self.alpha = alpha
        self.epsilon = epsilon

    def update(self, old_state, action, new_state, reward):
        """
        Update Q-learning model, given an old state, an action taken
        in that state, a new resulting state, and the reward received
        from taking that action.
        """
        # convert states to tuples of only the edges of the board
        old_state_edges = tuple(state_edges(old_state))
        # new_state_edges = tuple(state_edges(new_state))

        old = self.get_q_value(old_state_edges, action)
        best_future = self.best_future_reward(new_state)
        self.update_q_value(old_state_edges, action, old, reward, best_future)
    
    def get_q_value(self, state, action):
        """
        Return the Q-value for the state `state` and the action `action`.
        If no Q-value exists yet in `self.q`, return 0.
        """
        # if the state-action pair is not in the dictionary, return 0
        if (tuple(state), action) not in self.q:
            return 0
        else:
            return self.q[(tuple(state), action)]
    
    def update_q_value(self, state, action, old_q, reward, future_rewards):
        
        """
        Update the Q-value for the state `state` and the action `action`
        given the previous Q-value `old_q`, a current reward `reward`,
        and an estiamte of future rewards `future_rewards`.

        Use the formula:

        Q(s, a) <- old value estimate
                + alpha * (new value estimate - old value estimate)

        where `old value estimate` is the previous Q-value,
        `alpha` is the learning rate, and `new value estimate`
        is the sum of the current reward and estimated future rewards.
        """
        # get old value estimate
        new_value_estimate = reward + future_rewards
        self.q[(tuple(state), action)] = old_q + self.alpha * (new_value_estimate - old_q)
    
    def best_future_reward(self, state):
        """
        Given a state `state` of 4 elements, consider all possible `(state, action)`
        pairs available in that state and return the maximum of all
        of their Q-values.

        Use 0 as the Q-value if a `(state, action)` pair has no
        Q-value in `self.q`. If there are no available actions in
        `state`, return 0.

        # problem: all possible state action pairs
        also depend on the player's hand, which is not included 
        in the state representation. SOLVED through available_actions.
        """

        # if there are no available actions, return 0
        actions = available_actions(state)
        if len(actions) == 0:
            return 0
        
        # if there are available actions, return the max Q-value
        # use 0 as the q-value if the pair is not in the dictionary
        else:
            simple_state_edges = tuple(state_edges(state))
            # /Q: Am I returning 0 for all actions that are not in the dictionary??
            return max([self.get_q_value(simple_state_edges, action) for action in actions])

    
    def choose_action(self, state, epsilon=True):
        """
        Given a state `state`, return an action `(i, j)` to take.
        Includes e-greedy action selection.

        If `epsilon` is `False`, then return the best action
        available in the state (the one with the highest Q-value,
        using 0 for pairs that have no Q-values).

        If `epsilon` is `True`, then with probability
        `self.epsilon` choose a random available action,
        otherwise choose the best action available.

        If multiple actions have the same Q-value, any of those
        options is an acceptable return value.
        """
        # if epsilon is false, return the best action available
        if epsilon == False:
            # PROBABLY THIS IS A BUGGY COMPREHENSION; using both versions of the state
            return max(available_actions(state), key=lambda action: self.get_q_value( state_edges(state), action))
        
        # if epsilon is true, choose a random action with probability epsilon
        else:
            if random.random() < self.epsilon:
                return random.choice(list(available_actions(state)))
            else:
                return max(available_actions(state), key=lambda action: self.get_q_value(state_edges(state), action))
            

#%% training

def train(n):
    """
    Train an AI by playing `n` games against itself.
    """
    # initialize AI
    player = QAgent()

    # play `n` games

    for i in range(n):

        print(f"Playing training game {i + 1}")
        # initialize a new game
        game = dominoes.Game.new(starting_domino = dominoes.Domino(6, 6))
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

            # choose an action to take based on the current state
            action = player.choose_action(state)
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
                # points signals the winning team; if 0 and 2 win, points is positive
                # if 1 and 3 win, points is negative
                points = game.result.points
                # if the winning team is 0 and 2, reward is 1

                # update Q values for each of the 4 players
                for player_num in range(4):
                    if player_num == 0 or player_num == 2:
                        player.update(
                            last[player_num]["state"],
                            last[player_num]["action"],
                            new_state,
                            points
                        )
                    else:
                        player.update(
                            last[player_num]["state"],
                            last[player_num]["action"],
                            new_state,
                            -points
                        )
                break

            # If game is continuing, no rewards yet for any of the players

            elif last[game.turn]["state"] is not None:
                player.update(
                    last[game.turn]["state"],
                    last[game.turn]["action"],
                    new_state,
                    0
                )
    print("Done training")

    # Return the trained AI
    return player

#%% playing against agent

def play_against_ai(ai):
    raise NotImplementedError

#%%