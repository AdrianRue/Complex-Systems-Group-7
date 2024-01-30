import pytest
import numpy as np
from CellularAutomaton import CellularAutomaton

# Define a mock density function for testing
def mock_density_func(i, j):
    return 1.0

# Test cases for the CellularAutomaton class
class TestCellularAutomaton:
    @pytest.fixture
    def automaton(self):
        size = 10  
        agent_probs = [0.85, 0.15]  
        proto_size = 20
        star_size = 100
        return CellularAutomaton(size, agent_probs, proto_size, star_size)

    def test_initialization(self, automaton):
        assert automaton.size > 0
        assert automaton.proto_size > 0
        assert automaton.star_size > 0
        assert isinstance(automaton.groups, list)
        assert automaton.star == 10
        assert automaton.dissipation == 30

    def test_get_density(self, automaton):
        i, j = 5, 5 
        radius = 3 
        density = automaton.get_density(i, j, radius)
        print(type(density))
        assert isinstance(density, np.int32)

    def test_neighbours(self, automaton):
        i, j = 5, 5
        radius = 3
        states = [1, 2, 3]  
        neighbour_list = automaton.neighbours(i, j, radius, states)
        assert isinstance(neighbour_list, list)

    def test_update(self, automaton):
        frame = 0 
        grid_states = automaton.update(frame)
        assert isinstance(grid_states, np.ndarray)
        
    def test_get_grid_states(self, automaton):
        grid_states = automaton.get_grid_states()
        assert isinstance(grid_states, np.ndarray)  

if __name__ == "__main__":
    pytest.main()
