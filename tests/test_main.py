import pytest

from main import simulate

def test_simulate_valid_input():
    # Test with valid inputs
    try:
        simulate(100, 0.15, 35, 200)
    except Exception as e:
        pytest.fail(f"Unexpected error: {e}")

def test_simulate_invalid_grid_size():
    # Grid size must be a positive integer
    with pytest.raises(AssertionError):
        simulate(-1, 0.15, 35, 200)

def test_simulate_invalid_prob_gas():
    # Probability of gas must be between 0 and 1
    with pytest.raises(AssertionError):
        simulate(100, -0.1, 35, 200)
    with pytest.raises(AssertionError):
        simulate(100, 1.1, 35, 200)

def test_simulate_invalid_proto_size():
    # Proto size must be a positive integer and less than or equal to N^2
    with pytest.raises(AssertionError):
        simulate(100, 0.15, -1, 200)
    with pytest.raises(AssertionError):
        simulate(100, 0.15, 10001, 200)

def test_simulate_invalid_star_size():
    # Star size must be a positive integer and less than or equal to N^2
    with pytest.raises(AssertionError):
        simulate(100, 0.15, 35, -1)
    with pytest.raises(AssertionError):
        simulate(100, 0.15, 35, 10001)
