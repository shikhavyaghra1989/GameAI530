import numpy as np
from enum import Enum, IntEnum, auto
import typing

from multiprocessing import Pool
from functools import partial
import random
import math
import numba
from copy import deepcopy

from chainreaction.game import *
from chainreaction.positions import *
from chainreaction.board import *
from chainreaction.minimax import *
from chainreaction.mcts import *
from chainreaction.four_players import *

from experiments.utils import *

from tqdm import tqdm


from experiments import team_experiments

if __name__ == '__main__':
    pool = Pool(8)
    team_experiments.run_experiments(pool, 50)