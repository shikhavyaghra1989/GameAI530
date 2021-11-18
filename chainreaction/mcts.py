import numpy as np
import numba

from copy import deepcopy
from typing import *

from chainreaction.game import *
from chainreaction.board import *
from chainreaction.config import *


def next_viable_player(player, utilities):
    next_player = player.next_player()
    while utilities[next_player.get_zero_indexed_player_idx()] == 0:
        next_player = next_player.next_player()

    return next_player

def get_scores(state):
    utilities = board_utility(state.atom_type)
    scores = utilities / np.sum(utilities)
    assert np.max(scores) <= 1.0
    return scores

class MCTSNode():
    def __init__(self, state: Board, parent, parent_action, player):
        self.state: Board = state
        self.is_state_terminal = is_terminal(state.atom_type)
        self.parent: MCTSNode = parent
        self.parent_action = parent_action
        self.children: List[MCTSNode] = []
        self.player = player

        self._cumulative_scores = np.zeros((Players.num_players()), dtype=np.float32)
        self._number_of_visits = 0

        self._untried_actions = None
        self._untried_actions = self.untried_actions()

    def untried_actions(self):
        self._untried_actions = self.get_legal_actions(self.state, self.player)
        return self._untried_actions

    def q(self):
        return self._cumulative_scores

    def n(self):
        return self._number_of_visits

    def expand(self):
        pass

    def rollout(self):
        curr_rollout_state = self.state.get_copy()
        curr_player = deepcopy(self.player)
        is_curr_rollout_state_terminal = self.is_state_terminal
        while not is_curr_rollout_state_terminal:
            possible_moves = self.get_legal_actions(curr_rollout_state, curr_player)
            action = self.rollout_policy(possible_moves)
            curr_rollout_state, curr_player, _, is_curr_rollout_state_terminal = game_step(curr_rollout_state, curr_player, action)
            
        return get_scores(curr_rollout_state)

    def backpropagate(self, result):
        pass

    def is_fully_expanded(self):
        return len(self._untried_actions) == 0

    def best_child(self):
        pass

    def rollout_policy(self, possible_moves):    
        return possible_moves[np.random.randint(len(possible_moves))]

    def _tree_policy(self):
        current_node = self
        while not current_node.is_state_terminal:
            if not current_node.is_fully_expanded():
                return current_node.expand()
            else:
                current_node = current_node.best_child()
        return current_node

    def best_action(self):
        simulation_no = mcts_max_simulations
        for i in range(simulation_no):
            v = self._tree_policy()
            reward = v.rollout()
            v.backpropagate(reward)
        
        return self.best_child(c_param=0.)

    def get_legal_actions(self, state, player): 
        '''
        Modify according to your game or
        needs. Constructs a list of all
        possible actions from current state.
        Returns a list.
        '''
        valid_moves_arr = allowed_moves(state, player)
        valid_moves = []
        for i in range(valid_moves_arr[0].shape[0]):
            p = valid_moves_arr[0][i]
            q = valid_moves_arr[1][i]
            valid_moves.append((p, q))

        return valid_moves


class MCTSNormalNode(MCTSNode):
    def __init__(self, state, parent, parent_action, player):
        super().__init__(state, parent, parent_action, player)

    def expand(self):
        action = self._untried_actions.pop()
        atom_type = self.state.atom_type[action[0], action[1]]
        player_for_atom_type = Players(atom_type)
        if player_for_atom_type.is_union_player():
            child_node = MCTSChanceNode(self.state, self, action, self.player)
            self.children.append(child_node)
            return child_node
        
        else:
            next_state = do_move(Board.get_copy(self.state), action[0], action[1], self.player)
            next_state_utilities = board_utility(self.state.atom_type)
            next_player = next_viable_player(self.player, next_state_utilities)
            child_node = MCTSNormalNode(
                next_state, parent=self, parent_action=action, player=next_player
            )

            self.children.append(child_node)
            return child_node

    def backpropagate(self, result):
        self._number_of_visits += 1
        self._cumulative_scores += result
        if self.parent:
            self.parent.backpropagate(result)

    def best_child(self, c_param=0.1):
        choices_weights = ( (c.q() / c.n()) + c_param * np.sqrt((2 * np.log(self.n()) / c.n())) for c in self.children )
        choices_weights = map(lambda w: w[self.player.get_zero_indexed_player_idx()], choices_weights)
        res = np.argmax(choices_weights)
        return self.children[res]


class MCTSChanceNode(MCTSNode):

    def __init__(self, state, parent, parent_action, player):
        super().__init__(state, parent, parent_action, player)
        self._untried_actions = []
        self.decay_probs = decay_probs

        action = self.parent_action
        row_idx, col_idx = action
        atom = Players(self.state.atom_type[row_idx, col_idx])
        P_a, P_b = atom.get_union_player_members()

        # No change child
        next_state = do_move(self.state.get_copy(), row_idx, col_idx, self.player)
        next_player = next_viable_player(self.player, board_utility(next_state.atom_type))
        child_node = MCTSNormalNode(next_state, self, action, next_player)
        self.children.append(child_node)

        # P_a change child
        # P_a change
        next_state = self.state.get_copy()
        next_state.atom_type[row_idx, col_idx] = P_a.value
        next_state = do_move(next_state, row_idx, col_idx, P_a)
        next_player = next_viable_player(self.player, board_utility(next_state.atom_type))
        child_node = MCTSNormalNode(next_state, self, action, next_player)
        self.children.append(child_node)

        # P_b change child
        # P_b change
        next_state = self.state.get_copy()
        next_state.atom_type[row_idx, col_idx] = P_b.value
        next_state = do_move(next_state, row_idx, col_idx, P_b)
        next_player = next_viable_player(self.player, board_utility(next_state.atom_type))
        child_node = MCTSNormalNode(next_state, self, action, next_player)
        self.children.append(child_node)

    def is_fully_expanded(self):
        return True
    
    def expand(self):
        # assume chance node is always fully expanded
        pass

    def backpropagate(self, result):
        self._number_of_visits += 1
        self._cumulative_scores +=  result
        if self.parent:
            self.parent.backpropagate(result)

    def best_child(self, c_param=0.1):
        choice = np.random.choice(3, 1, p=self.decay_probs)[0]
        return self.children[choice]
