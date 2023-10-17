"""
this file is a necessary part of the dominoes_lib package. it is used to 
import all of the modules in the dominoes subdirectory correctly. It follows
standard python conventions for importing modules.

Q : is this importing from the true dominoes library or from mine? test it easily
"""

from dominoes import players
from dominoes import search
from dominoes.board import Board
from dominoes.domino import Domino
from dominoes.exceptions import EmptyBoardException
from dominoes.exceptions import EndsMismatchException
from dominoes.exceptions import GameInProgressException
from dominoes.exceptions import GameOverException
from dominoes.exceptions import NoSuchDominoException
from dominoes.exceptions import NoSuchPlayerException
from dominoes.exceptions import SeriesOverException
from dominoes.game import Game
from dominoes.hand import Hand
from dominoes.result import Result
from dominoes.series import Series
from dominoes.skinny_board import SkinnyBoard
