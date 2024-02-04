import numpy as np
import pytest
from Agent import Agent, find_nearest  # Adjust the import as necessary to fit your project structure

def test_agent_initialization():
    state = np.int32(1)
    agent = Agent(state)
    assert agent.state == state
    assert agent.group is None
    assert agent.position is None
    assert agent.days_dissipate == 0
    assert agent.center_group is None

def test_find_nearest():
    array = [-1, 0, 1]
    value = 0.9
    expected = 1
    assert find_nearest(array, value) == expected

def test_move_center():
    pos_c_i, pos_c_j = 5, 5
    pos_agent_i, pos_agent_j = 3, 3
    size = 10
    agent = Agent(np.int32(1))
    new_i, new_j = agent.move_center(pos_c_i, pos_c_j, pos_agent_i, pos_agent_j, size)
    assert new_i == 4 and new_j == 4  # Assuming move towards center

def test_dissipate():
    # This test might need a mock group with a center and size
    size = 10
    pos_agent_i, pos_agent_j = 8, 8
    agent = Agent(np.int32(1))
    agent.center_group = (5, 5)  # Example center; adjust as needed
    agent.group = type('MockGroup', (object,), {'center': (5, 5), 'size': size})()  # Mock group
    new_i, new_j = agent.dissipate(pos_agent_i, pos_agent_j, size)