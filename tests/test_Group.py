import numpy as np
import pytest
from Group import Group  
from Agent import Agent

def test_group_initialization():
    agent = Agent(np.int32(2))
    star_size = 10
    star = 5
    dissipation = 15
    group = Group(agent, star_size, star, dissipation)
    assert len(group.agents) == 1
    assert group.star_size == star_size
    assert group.star == star
    assert group.dissipation == dissipation
    assert group.state == 2
    assert agent.state == group.state
    assert agent.group is group

def test_group_append():
    agent1 = Agent(np.int32(2))
    agent2 = Agent(np.int32(2))
    group = Group(agent1, 10, 5, 15)
    group.append(agent2)
    assert len(group.agents) == 2
    assert agent2 in group.agents
    assert agent2.state == group.state
    assert agent2.group is group

def test_group_calculate_center():
    agent1 = Agent(np.int32(2))
    agent1.position = (0, 0)
    agent2 = Agent(np.int32(2))
    agent2.position = (10, 10)
    group = Group(agent1, 10, 5, 15)
    group.append(agent2)
    center = group.calculate_center()
    assert center == (5, 5)

def test_group_update():
    agent = Agent(np.int32(2))
    agent.position = (0, 0)
    group = Group(agent, 1, 0, 0)
    group.update()
    assert group.state == 3
    assert group.steps == 1

def test_group_merge():
    agent1 = Agent(np.int32(2))
    agent1.position = (0, 0)
    group1 = Group(agent1, 10, 5, 15)
    
    agent2 = Agent(np.int32(2))
    agent2.position = (10, 10)
    group2 = Group(agent2, 10, 5, 15)
    
    group1.merge(group2)
    assert len(group1.agents) == 2
    assert group2.merged
    assert agent2.group is group1