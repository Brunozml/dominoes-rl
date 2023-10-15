"""
this script contains my first attempt at a q-learning agent. The state of the board is extremely simplified;
we only consider the edges of the board, and the tiles in the player's hand. 

Missing features:
    - Integration with the dominoes_lib package. I can use the players.py file as inspiration

Missing functionality:
    - get_q_value function
    - best_future_reward function
    - choose_action function


"""

import math
import random
import dominoes_lib


class q_agent:
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
        old = self.get_q_value(old_state, action)
        best_future = self.best_future_reward(new_state)
        self.update_q_value(old_state, action, old, reward, best_future)
    
    def get_q_value(self, state, action):
        """
        Return the Q-value for the state `state` and the action `action`.
        If no Q-value exists yet in `self.q`, return 0.
        """
        raise NotImplementedError
    
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
        Given a state `state`, consider all possible `(state, action)`
        pairs available in that state and return the maximum of all
        of their Q-values.

        Use 0 as the Q-value if a `(state, action)` pair has no
        Q-value in `self.q`. If there are no available actions in
        `state`, return 0.
        """
        raise NotImplementedError
    
    def choose_action(self, state, epsilon=True):
        """
        Given a state `state`, return an action `(i, j)` to take.

        If `epsilon` is `False`, then return the best action
        available in the state (the one with the highest Q-value,
        using 0 for pairs that have no Q-values).

        If `epsilon` is `True`, then with probability
        `self.epsilon` choose a random available action,
        otherwise choose the best action available.

        If multiple actions have the same Q-value, any of those
        options is an acceptable return value.
        """
        raise NotImplementedError


#%% 
    def __call__(self, game):
        # do not perform a potentially slow operation if it is
        # too early in the game or if there is only one valid move
        if len(game.moves) < self._start_move or len(game.valid_moves) == 1:
            return

        if self._sample_size == float('inf'):
            # by default consider all hands the other players could possibly have
            hands = game.all_possible_hands()
        else:
            # otherwise obtain a random sample
            hands = (game.random_possible_hands() for _ in range(self._sample_size))

        # iterate over the selected possible hands
        counter = collections.Counter()
        for h in hands:
            # do not modify the original game
            game_copy = copy.deepcopy(game)

            # set the possible hands
            game_copy.hands = h

            # for performance
            game_copy.skinny_board()

            # run alphabeta and record the optimal move
            counter.update([
                dominoes.search.alphabeta(game_copy, player=self._player)[0][0]
            ])

        # prefer moves that are more frequently optimal
        game.valid_moves = tuple(sorted(game.valid_moves, key=lambda m: -counter[m]))
