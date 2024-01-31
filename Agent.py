import numpy as np

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
        assert isinstance(state, (np.int32, np.int64)), "State must be an integer"
        self.state = state
        self.group = None
        self.position = None
        self.days_dissipate = 0



    def move(self, i, j, density_grid, grid):
        """
        Returns the new position of the agent if the agent is not dissipating

        :param i: Vertical position of the agent
        :param j: Horizontal position of the agent
        :param grid: Grid with the densities of the agents
        :return: New position of the agent
        """

        movement = []
        densities = []
        for di in range(-1, 2):
            for dj in range(-1, 2):
                if di == 0 and dj == 0:
                    continue

                ni, nj = (i + di) % grid.shape[0], (j + dj) % density_grid.shape[1]
                movement.append((ni, nj))
                densities.append(density_grid[ni, nj] * (grid[ni, nj].state == 0))
        densities_sum = np.sum(densities)

        if self.state == 1:
            if densities_sum == 0:
                direction = np.random.choice(range(len(movement)))

            else:
                probabilities = np.array(densities) / densities_sum
                direction = np.random.choice(range(len(movement)), p=probabilities)

            return movement[direction]

        else:
            direction = np.argmax(densities)
            movement = movement[direction]

            if density_grid[i, j] < density_grid[movement]:
                return movement



    def move_center(self, pos_c_i, pos_c_j, pos_agent_i, pos_agent_j, size):

        # Compute vector
        direction = [pos_agent_i - pos_c_i, pos_agent_j - pos_c_j]

        # Round to nearest integer
        direction[0] = find_nearest([-1, 0, 1], direction[0])
        direction[1] = find_nearest([-1, 0, 1], direction[1])


        pos_agent_i -= direction[0]
        pos_agent_j -= direction[1]

        # Wrap around if out of bounds
        pos_agent_i %= size
        pos_agent_j %= size

        return pos_agent_i, pos_agent_j


    def dissipate(self, pos_agent_i, pos_agent_j, size):
        """
        Returns the new position of the agent if dissipation is happening

        :param pos_c_i: Vertical position of the center of the group
        :param pos_c_j: Horizontal position of the center of the group
        :param pos_agent_i: Vertical position of the agent
        :param pos_agent_j: Horizontal position of the agent
        :param size: Size of the grid
        :return: New position of the agent
        """

        pos_c_i, pos_c_j = self.group.center

        # Compute vector
        movement = [pos_agent_i - pos_c_i, pos_agent_j - pos_c_j]

        # Round to nearest integer
        movement[0] = find_nearest([-1, 0, 1], movement[0])
        movement[1] = find_nearest([-1, 0, 1], movement[1])

        # Possible directions
        directions = [
                [-1, 0], [1, 0], [0, -1], [0, 1], [-1, -1], [-1, 1], [1, -1], [1, 1]
            ]

        # If the direction is 0,0, choose a random direction
        if movement[0] == 0 and movement[1] == 0:
            # Choose a random direction
            direction = np.random.choice(range(len(directions)))
            movement = directions[direction]


        if abs(self.center_group[0] - pos_agent_i) > self.group.size / 4:
            pos_agent_i -= movement[0]
        else:
            pos_agent_i += movement[0]

        if abs(self.center_group[1] - pos_agent_j) > self.group.size / 4:
            pos_agent_j -= movement[1]
        else:
            pos_agent_j += movement[1]
            
        # New position of the agent
        # pos_agent_i += movement[0]
        # pos_agent_j += movement[1]

        # Wrap around if out of bounds
        pos_agent_i %= size
        pos_agent_j %= size

        return pos_agent_i, pos_agent_j
    



def find_nearest(array, value):
    """
    Returns the nearest value in an array to a given value. Used in the dissipate function to
    determine the direction of the agent.

    :param array: Array to search in
    :param value: Value to search for
    :return: Closest value in the array to the given value
    """
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return array[idx]

