
import dominoes
from dominoes.players import *
from dominoes.q_learner import QLearner
from dominoes.train import train
from dominoes.omniscient import Omniscient

PLAYERS = [QLearner(), RandomPlayer(), Omniscient(), QLearner()]

train(PLAYERS, n=100, tiles_per_hand= 2, verbose = True)