import unittest
from q_agent import *
import dominoes_lib as dominoes

class TestQAgent(unittest.TestCase):
    def test_train(self):
        # test that the train function returns a Q-learning agent
        q_agent = train(n=1)
        self.assertIsInstance(q_agent, QAgent)


def test_get_q_value_returns_zero_if_state_action_pair_not_in_q(self):
    # test that get_q_value returns 0 if the state-action pair is not in q
    q_agent = QAgent()
    state = [0, 0, 0, 0]
    action = (0, 0)
    q_value = q_agent.get_q_value(state, action)
    self.assertEqual(q_value, 0)

def test_get_q_value_returns_correct_value_if_state_action_pair_in_q(self):
    # test that get_q_value returns the correct value if the state-action pair is in q
    q_agent = QAgent()
    state = [0, 0, 0, 0]
    action = (0, 0)
    q_agent.q[(tuple(state), action)] = 1.0
    q_value = q_agent.get_q_value(state, action)
    self.assertEqual(q_value, 1.0)

def test_choose_action_returns_valid_action(self):
    # test that choose_action returns a valid action
    q_agent = QAgent()
    state = [0, 0, 0, 0]
    action = q_agent.choose_action(state)
    self.assertIn(action, available_actions(state))