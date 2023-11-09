"""
objective: compare training times for different sizes of the game tree
"""

from dominoes.players import *
from dominoes.q_learner import QLearner
from dominoes.train import train
from dominoes.omniscient import Omniscient
# import time module to compare times
import time


PLAYERS = [QLearner(), RandomPlayer(), RandomPlayer(), RandomPlayer()]

for i in range(2,8):
    # start timer
    start = time.time()
    train(PLAYERS, n=10_000, tiles_per_hand= i, verbose = False)
    # end timer
    end = time.time()
    # print time elapsed
    print(round(end - start,5))
