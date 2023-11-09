"""
Q-learning player for dominoes game. constant epsilon exploration.
"""

# import Player class from player.py
from dominoes.players import Player
import random as rand

#%% helper functions for class

def simple_state(game):
    if len(game.board) == 0:
        return [None, None, game.turn, game.hands]
    
    return [game.board.left_end(), game.board.right_end(), game.turn, game.hands]


def state_edges(state):
    """
    returns the edges of the board as a tuple.
    """
    if state is None:
        return 
    # TO-DO: re-organize so that there is no need to have "two states".
    # this is a hacky solution to the problem, but not ideal for debugging.
    return (state[0], state[1])

# TODO: integrate this with game.valid_moves attribute. they are doing the same thing


def available_actions(state):
    """
    uses game state to return list of available actions for the current
    player
    """
    left_end, right_end, turn, hands = state
    # handle case when no dominoes have been played yet
    if left_end is None:
        return tuple((domino, True) for domino in hands[turn])
    
    moves = set()
    for domino in hands[turn]:
        if left_end in domino:
            moves.add((domino, True))
        if right_end in domino and left_end != right_end:
            moves.add((domino, False))
    return tuple(moves)


def rewards(game):
    """
    input: finished game (game.return is not None)

    output: reward per player??
    """
    raise NotImplementedError



#%%  create instance of QLearner using abstract player class as parent
class QLearner(Player):

    '''
        Initialize AI with an empty Q-learning dictionary,
        an alpha (learning) rate, and an epsilon rate.

        The Q-learning dictionary maps `(state, action)`
        pairs to a Q-value (a number).
         - `state` is a tuple of the tiles at the edge of the board, e.g. (1,4)
         - `action` is a tuple `(tile, side)` for an action
    '''

    def __init__(self, alpha=0.5, epsilon=0.1):
        super().__init__('Q-learning Player')
        self.q = dict()
        self.alpha = alpha
        self.epsilon = epsilon
        self.training_error = []

    def __call__(self, game, epsilon = True):
        """
        Given a game, choose a move to make based on the current state of the game.
        """
        # get current state
        state = simple_state(game).copy()

        # get all available actions
        actions = available_actions(state)

        # choose an action to take based on the current state
        action = self._choose_action(state, epsilon= epsilon)
        # place the optimal move at the beginning of game.valid_moves,
        # while leaving the rest of the ordering unchanged.

        # # !!! probably breaking something here
        sorted_moves = (action,) + tuple(m for m in actions if m != action)
        game.valid_moves = sorted_moves

        return action

    def update(self, old_state, action, new_state, reward):
        """
        Update Q-learning model, given an old state, an action taken
        in that state, a new resulting state, and the reward received
        from taking that action.
        """
                # check if old_state is None
        if old_state is None:
            return

        # convert states to tuples of only the edges of the board
        old_state_edges = tuple(state_edges(old_state))
        # new_state_edges = tuple(state_edges(new_state))

        old = self._get_q_value(old_state_edges, action)
        best_future = self._best_future_reward(new_state)
        self._update_q_value(old_state_edges, action, old, reward, best_future)

    def _get_q_value(self, state, action):
        """
        Return the Q-value for the state `state` and the action `action`.
        If no Q-value exists yet in `self.q`, return 0.
        """
        # if the state-action pair is not in the dictionary, return 0
        if (tuple(state), action) not in self.q:
            return 0
        else:
            return self.q[(tuple(state), action)]

    def _update_q_value(self, state, action, old_q, reward, future_rewards):
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
        self.q[(tuple(state), action)] = old_q + \
            self.alpha * (new_value_estimate - old_q)
        self.training_error.append(abs(new_value_estimate - old_q))

    def _best_future_reward(self, state):
        """
        Given a state `state` of 4 elements, consider all possible `(state, action)`
        pairs available in that state and return the maximum of all
        of their Q-values.

        Use 0 as the Q-value if a `(state, action)` pair has no
        Q-value in `self.q`. If there are no available actions in
        `state`, return 0.
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
            return max([self._get_q_value(simple_state_edges, action) for action in actions])

    def _choose_action(self, state, epsilon=True):
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
            return max(available_actions(state), key=lambda action: self._get_q_value(state_edges(state), action))

        # if epsilon is true, choose a random action with probability epsilon
        else:
            if rand.random() < self.epsilon:
                return rand.choice(list(available_actions(state)))
            else:
                return max(available_actions(state), key=lambda action: self._get_q_value(state_edges(state), action))