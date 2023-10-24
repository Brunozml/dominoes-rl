"""
This file contains the Player class and some simple player implementations.
"""
# import ABC
from abc import ABC, abstractmethod
import random as rand


# implement an abstract player class with an abstract method for choosing an action and a method for updating the player's state
class Player(ABC):
    def __init__(self, name):
        self.name = name

    @abstractmethod
    def __call__(self, game):
        raise NotImplementedError

    # def update_state(self, state):
    #     self.hand = state[0]
    #     self.score = state[1]

    @abstractmethod
    def update(self, old_state, action, new_state, reward):
        pass  # do nothing by default

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    # def __eq__(self, other):
    #     if isinstance(other, Player):
    #         return self.name == other.name
    #     return False


# %% simple players

    def __call__(self, game):
        """
        Given a game, choose a move to make based on the current state of the game.
        Doesn't modify game.valid_moves; returns the chosen move.
        """
        return game.valid_moves[0]

    def update(self, old_state, action, new_state, reward):
        pass  # do nothing by default

# define random player class


class RandomPlayer(Player):
    def __init__(self):
        super().__init__('Random Player')

    def __call__(self, game):
        """
        Given a game, choose a move to make based on the current state of the game. 
        Modifies game.valid_moves and returns the chosen move.
        """
        # choose a random action
        game.valid_moves = tuple(
            sorted(game.valid_moves, key=lambda _: rand.random()))

        return game.valid_moves[0]

    def update(self, old_state, action, new_state, reward):
        pass  # do nothing by default


class BotaGorda(Player):
    def __init__(self):
        super().__init__('Bota Gorda')

    def __call__(self, game):
        """
        Given a game, Prefers to play dominoes with higher point values.
        Modifies game.valid_moves and returns the chosen move.
        """
        # get current state

        # choose a random action
        game.valid_moves = tuple(
            sorted(game.valid_moves, key=lambda m: -(m[0].first + m[0].second)))

        return game.valid_moves[0]

    def update(self, old_state, action, new_state, reward):
        pass  # do nothing by default


class DoubleLover(Player):
    def __init__(self):
        super().__init__('Double Lover')

    def __call__(self, game):
        """
        Given a game, Prefers to play dominoes with same value on both sides.
        Modifies game.valid_moves and returns the chosen move.
        """
        game.valid_moves = tuple(
            sorted(game.valid_moves, key=lambda m: m[0].first != m[0].second))

        return game.valid_moves[0]

    def update(self, old_state, action, new_state, reward):
        pass  # do nothing by default
