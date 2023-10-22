'''
Players are Python objects with a ``__call__`` method
defined to accept a Game instance as the sole argument.
Players return None, and leave the input Game unmodified,
except for its valid_moves attribute. This value may be
replaced with another tuple containing the same moves,
but sorted in decreasing order of preference. Players
may be applied one after another for easy composability.

'''
#%% imports
import collections
import copy
import dominoes
import random as rand
import copy

#%% heuristic players
def identity(game):
    '''
    Leaves move preferences unchanged.

    :param Game game: game to play
    :return: None
    '''
    return


class counter:
    '''
    Prefers moves in the same order as the passed-in player. Keeps
    a counter of the amount of times that this player gets called.
    An instance of this class must first be initialized before it
    can be called in the usual way.

    :param callable player: player that determines the move preferences of
                            this player. The identity player is the default.
    :param str name: the name of this player. The default is the name
                     of this class.
    :var int count: the amount of times that this player has been called.
    :var str __name__: the name of this player.
    '''

    def __init__(self, player=identity, name=None):
        self.count = 0
        self._player = player
        if name is None:
            self.__name__ = type(self).__name__
        else:
            self.__name__ = name

    def __call__(self, game):
        self.count += 1
        return self._player(game)


def random(game):
    '''
    Prefers moves randomly.

    :param Game game: game to play
    :return: None
    '''
    game.valid_moves = tuple(
        sorted(game.valid_moves, key=lambda _: rand.random()))


def random_player(game):
    '''
    Prefers moves randomly.

    :param Game game: game to play
    :return: None
    '''
    game.valid_moves = tuple(
        sorted(game.valid_moves, key=lambda _: rand.random()))


def reverse(game):
    '''
    Reverses move preferences.

    :param Game game: game to play
    :return: None
    '''
    game.valid_moves = tuple(reversed(game.valid_moves))


def bota_gorda(game):
    '''
    Prefers to play dominoes with higher point values.

    :param Game game: game to play
    :return: None
    '''
    game.valid_moves = tuple(
        sorted(game.valid_moves, key=lambda m: -(m[0].first + m[0].second)))


def double(game):
    '''
    Prefers to play doubles.

    :param Game game: game to play
    :return: None
    '''
    game.valid_moves = tuple(
        sorted(game.valid_moves, key=lambda m: m[0].first != m[0].second))


class omniscient:
    '''
    Prefers to play the move that maximizes this player's final score,
    assuming that all other players play with the same strategy. This
    player "cheats" by looking at all hands to make its decision. An
    instance of this class must first be initialized before it can be
    called in the usual way.

    :param int start_move: move number at which to start applying this
                           player. If this player is called before the
                           specified move number, it will have no effect.
                           Moves are 0-indexed. The default is 0.
    :param callable player: player used to sort moves to be explored
                            in the underlying call to alphabeta search.
                            Ordering better moves first may significantly
                            reduce the amount of moves that need to be
                            explored. The identity player is the default.
    :param str name: the name of this player. The default is the name
                     of this class.
    :var str __name__: the name of this player
    '''

    def __init__(self, start_move=0, player=identity, name=None):
        self._start_move = start_move
        self._player = player
        if name is None:
            self.__name__ = type(self).__name__
        else:
            self.__name__ = name

    def __call__(self, game):
        # do not perform a potentially slow operation if it is
        # too early in the game or if there is only one valid move
        if len(game.moves) < self._start_move or len(game.valid_moves) == 1:
            return

        # so that we don't modify the original game
        game_copy = copy.deepcopy(game)

        # for performance
        game_copy.skinny_board()

        # perform an alphabeta search to find the optimal move sequence
        moves, _ = dominoes.search.alphabeta(game_copy, player=self._player)

        # place the optimal move at the beginning of game.valid_moves,
        # while leaving the rest of the ordering unchanged
        game.valid_moves = (
            moves[0],) + tuple(m for m in game.valid_moves if m != moves[0])

#%% probabilistic search player
class probabilistic_alphabeta:
    '''
    This player repeatedly assumes the other players' hands, runs alphabeta search,
    and prefers moves that are most frequently optimal. It takes into account all
    known information to determine what hands the other players could possibly have,
    including its hand, the sizes of the other players' hands, and the moves played
    by every player, including the passes. An instance of this class must first be
    initialized before it can be called in the usual way.

    :param int start_move: move number at which to start applying this
                           player. If this player is called before the
                           specified move number, it will have no effect.
                           Moves are 0-indexed. The default is 0.
    :param int sample_size: the number of times to assign random possible
                            hands to other players and run alphabeta search
                            before deciding move preferences. By default
                            considers all hands that other players could
                            possibly have.
    :param callable player: player used to sort moves to be explored
                            in the underlying call to alphabeta search.
                            Ordering better moves first may significantly
                            reduce the amount of moves that need to be
                            explored. The identity player is the default.
    :param str name: the name of this player. The default is the name
                     of this class.
    :var str __name__: the name of this player
    '''

    def __init__(self, start_move=0, sample_size=float('inf'), player=identity, name=None):
        self._start_move = start_move
        self._sample_size = sample_size
        self._player = player
        if name is None:
            self.__name__ = type(self).__name__
        else:
            self.__name__ = name

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
            hands = (game.random_possible_hands()
                     for _ in range(self._sample_size))

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
        game.valid_moves = tuple(
            sorted(game.valid_moves, key=lambda m: -counter[m]))


"""
The state of the board is extremely simplified;
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
# %% helper functions for Q-agent. Should probably be located somewhere else.


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


# %% Q-learning agent
class QAgent:
    '''
        Initialize AI with an empty Q-learning dictionary,
        an alpha (learning) rate, and an epsilon rate.

        The Q-learning dictionary maps `(state, action)`
        pairs to a Q-value (a number).
         - `state` is a tuple of the tiles at the edge of the board, e.g. (1,4)
         - `action` is a tuple `(tile, side)` for an action
    '''

    def __init__(self, alpha=0.5, epsilon=0.1):
        self.q = dict()
        self.alpha = alpha
        self.epsilon = epsilon
        self.training_error = []

    def __call__(self, game):
        """
        Given a game, choose a move to make based on the current state of the game.
        """
        # get current state
        state = simple_state(game).copy()

        # get all available actions
        actions = available_actions(state)

        # choose an action to take based on the current state
        action = self._choose_action(state, epsilon=False)
        # place the optimal move at the beginning of game.valid_moves,
        # while leaving the rest of the ordering unchanged.

        # # !!! probably breaking something here
        sorted_moves = (action,) + tuple(m for m in actions if m != action)
        game.valid_moves = sorted_moves

        return action

    def _update(self, old_state, action, new_state, reward):
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

    def train(self, n=100, verbose=False):
        """
        TODO: write docstring
        """

        for i in range(n):

            if verbose is True:
                print(f"Playing training game {i + 1}")

            # initialize a new game
            game = dominoes.Game.new(starting_domino=dominoes.Domino(6, 6))
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
                action = self._choose_action(state)
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
                            self._update(
                                last[player_num]["state"],
                                last[player_num]["action"],
                                new_state,
                                points
                            )
                        else:
                            self._update(
                                last[player_num]["state"],
                                last[player_num]["action"],
                                new_state,
                                -points
                            )
                    break

                # If game is continuing, no rewards yet for any of the players

                elif last[game.turn]["state"] is not None:
                    self._update(
                        last[game.turn]["state"],
                        last[game.turn]["action"],
                        new_state,
                        0
                    )
        print("Done training")

        def train_series(self, n=1000, max_score = 150, verbose=False):
            """
            """
            raise NotImplementedError
        

