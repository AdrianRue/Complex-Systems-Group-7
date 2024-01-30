import numpy as np
import math

class Agent:
    """
    Class representing an agent

    Attributes
    ----------
    state : int
        State of the agent
    group : Group
        Group the agent belongs to
    position : tuple
        Position of the agent in the grid
    center_group : Tuple
        Location of the center of the group

    Methods
    -------
    move(get_density_func, i, j, size)
        Returns the new position of the agent
    dissipation(pos_c_i, pos_c_j, pos_agent_i, pos_agent_j, size)
        Returns the new position of the agent if dissipation is happening
    """
    def __init__(self, state):
        """
        Constructs a new agent

        :param state: State of the agent
        """
        assert isinstance(state, np.int32), "State must be an integer"
        self.state = state
        self.group = None
        self.position = None
        self.center_group = None

    def move(self, get_density_func, i, j, size):
        assert callable(get_density_func), "get_density_func must be a callable function"
        assert isinstance(i, int) and isinstance(j, int), "i and j must be integers"
        assert isinstance(size, int) and size > 0, "size must be a positive integer"

        directions = {
            'up': ((i - 1) % size, j),
            'down': ((i + 1) % size, j),
            'left': (i, (j - 1) % size),
            'right': (i, (j + 1) % size),
            'up-left': ((i - 1) % size, (j - 1) % size),
            'up-right': ((i - 1) % size, (j + 1) % size),
            'down-left': ((i + 1) % size, (j - 1) % size),
            'down-right': ((i + 1) % size, (j + 1) % size)
        }

        # Calculate densities for each direction
        densities = {dir: get_density_func(pos[0], pos[1]) for dir, pos in directions.items()}
        # print("Densities:", densities)  # Debug statement

        # Compute sum of densities
        density_sum = sum(densities.values())

        # Density has to be non-zero
        if density_sum != 0:
            # Compute probabilities for each direction
            probabilities = {dir: density / density_sum for dir, density in densities.items()}
            # print("Probabilities:", probabilities)  # Debug statement

            # Choose direction based on probabilities
            direction = np.random.choice(list(directions.keys()), p=list(probabilities.values()))
        else:
            # If density is zero, choose random direction
            direction = np.random.choice(list(directions.keys()))

        # print("Chosen direction:", direction)  # Debug statement
        return directions[direction]


    def dissipate(self, pos_c_i, pos_c_j, pos_agent_i, pos_agent_j, size):

        vec_i = pos_c_i - pos_agent_i
        vec_j = pos_c_j - pos_agent_j

        angle = math.degrees(math.atan(vec_i/vec_j))


        if  angle >= 337.5 or angle < 22.5:
            return (pos_agent_i - 1) % size, pos_agent_j
        elif angle >= 22.5 and angle < 67.5:
            return (pos_agent_i - 1) % size, (pos_agent_j + 1) % size
        elif angle >= 67.5 and angle < 112.5:
            return pos_agent_i, (pos_agent_j + 1) % size
        elif angle >= 112.5 and angle < 157.5:
            return (pos_agent_i + 1) % size, (pos_agent_j + 1) % size
        elif angle >= 157.5 and angle < 202.5:
            return (pos_agent_i + 1) % size, pos_agent_j
        elif angle >= 202.5 and angle < 247.5:
            return (pos_agent_i + 1) % size, (pos_agent_j - 1) % size
        elif angle >= 247.5 and angle < 292.5:
            return pos_agent_i, (pos_agent_j - 1) % size
        elif angle >= 292.5 and angle < 337.5:
            return (pos_agent_i - 1) % size, (pos_agent_j - 1) % size
        else:
            return pos_agent_i, pos_agent_j



