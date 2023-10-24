import dominoes.search
from dominoes.players import *
import copy

class Omniscient(Player):
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

    def __init__(self, start_move=0, player= dominoes.players.RandomPlayer, name=None):
        self._start_move = start_move
        self._player = player()
        if name is None:
            self.__name__ = type(self).__name__
        else:
            self.__name__ = name

    def __call__(self, game):
        # do not perform a potentially slow operation if it is
        # too early in the game or if there is only one valid move
        if len(game.moves) < self._start_move or len(game.valid_moves) == 1:
            return game.valid_moves[0]

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
        
        return game.valid_moves[0]

    def update(self, old_state, action, new_state, reward):
        pass