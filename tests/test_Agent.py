import pytest
import numpy as np
from Agent import Agent 

# Define a mock density function for testing
def mock_density_func(i, j):
    return 1.0 

# Test cases for the Agent class
class TestAgent:
    @pytest.fixture
    def agent(self):
        state = np.int32(1)
        return Agent(state)

    def test_move_function(self, agent):
        size = 10
        i, j = 5, 5
        move_result = agent.move(mock_density_func, i, j, size)
        assert isinstance(move_result, tuple)
        assert len(move_result) == 2
        assert isinstance(move_result[0], int) and isinstance(move_result[1], int)
        assert 0 <= move_result[0] < size
        assert 0 <= move_result[1] < size

    def test_dissipate_function(self, agent):
        size = 10
        pos_c_i, pos_c_j = 5, 5
        pos_agent_i, pos_agent_j = 4, 4
        dissipate_result = agent.dissipate(pos_c_i, pos_c_j, pos_agent_i, pos_agent_j, size)
        assert isinstance(dissipate_result, tuple)
        assert len(dissipate_result) == 2
        assert isinstance(dissipate_result[0], int) and isinstance(dissipate_result[1], int)
        assert 0 <= dissipate_result[0] < size
        assert 0 <= dissipate_result[1] < size

    def test_invalid_state(self):
        with pytest.raises(AssertionError):
            state = "invalid_state"
            Agent(state)

    def test_invalid_density_func(self, agent):
        with pytest.raises(AssertionError):
            get_density_func = "not_a_callable_function"
            agent.move(get_density_func, 0, 0, 10)

    def test_invalid_i_j_size(self, agent):
        with pytest.raises(AssertionError):
            agent.move(mock_density_func, 0.5, 0, 10)
        with pytest.raises(AssertionError):
            agent.move(mock_density_func, 0, 0.5, 10)
        with pytest.raises(AssertionError):
            agent.move(mock_density_func, 0, 0, -1)

# Run pytest
if __name__ == "__main__":
    pytest.main()
