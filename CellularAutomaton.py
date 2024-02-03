import numpy as np
from Group import Group
from Agent import Agent
from numba import jit

@jit(nopython=True, parallel=True)
def density_grid(states, radius=5):
    """
    Returns the density of agents in a given radius around a position

    :param states: States of the agents
    :param radius: Radius around the agent
    :return: Density of agents in a given radius around a position
    """

    size = states.shape
    # List with neighbours
    density = np.zeros(size)

    for i in range(states.shape[0]):
        for j in range(states.shape[1]):
            # Get neighbors
            for di in range(-radius, radius + 1):
                for dj in range(-radius, radius + 1):

                    # Skip the current cell
                    if di == 0 and dj == 0:
                        continue

                    # Ensure we wrap around the grid boundaries
                    ni, nj = (i + di) % states.shape[0], (j + dj) % states.shape[1]
                    density[i, j] += (states[ni, nj] * 100)
    return density

class CellularAutomaton:
    """
    Class representing a cellular automaton

    Attributes
    ----------
    size : int
        Size of the grid
    proto_size : int
        Size of the proto groups before they become a star group
    star_size : int
        Size of the star groups before they dissipate
    grid : numpy.ndarray
        Grid of agents
    groups : list
        List of groups
    star : int
        Time needed for a proto-star to become a star
    dissipation : int
        Time needed for a star to dissipate

    Methods
    -------
    get_density(i, j, radius=3)
        Returns the density of agents in a given radius around a position
    neighbours(i, j, radius, states=[1,2,3])
        Returns a list of neighbours in a given radius around a position
    update(frame)
        Updates the grid and groups
    get_grid_states()
        Returns the grid states

    """
    def __init__(self, size, agent_probs, proto_size, star_size, steps_dissipating):
        """
        Constructs a new cellular automaton

        :param size: Size of the grid
        :param agent_probs: Probabilities of an agent being in state 1
        :param proto_size: Size of the proto groups before they become a star group
        :param star_size: Size of the star groups before they dissipate
        """
        assert isinstance(size, int) and size > 0, "Size must be a positive integer"
        assert isinstance(proto_size, int) and proto_size > 0, "Proto size must be a positive integer"
        assert isinstance(star_size, int) and star_size > 0, "Star size must be a positive integer"
        assert isinstance(agent_probs, (list, np.ndarray)), "agent_probs must be a list or numpy array"
        assert isinstance(steps_dissipating, int) and steps_dissipating > 0, "Steps dissipating must be a positive integer"
        assert all(0 <= p <= 1 for p in agent_probs), "Probabilities in agent_probs must be between 0 and 1"

        self.size = size
        self.proto_size = proto_size
        self.star_size = star_size
        self.grid = np.array([[Agent(state) for state in row] for row in np.random.choice([0, 1], size*size, p=agent_probs).reshape(size, size)], dtype=Agent)
        self.groups = []
        self.star = 10
        self.dissipation = steps_dissipating

    def get_density(self, i, j, radius=3):
        """
        Returns the density of agents in a given radius around a position

        :param i: Vertical position of the agent
        :param j: Horizontal position of the agent
        :param radius: Radius around the agent
        :return: Density of agents in a given radius around a position
        """
        # List with neighbours
        density = 0

        # Get neighbors
        for di in range(-radius, radius + 1):
            for dj in range(-radius, radius + 1):

                # Skip the current cell
                if di == 0 and dj == 0:
                    continue

                # Ensure we wrap around the grid boundaries
                ni, nj = (i + di) % self.size, (j + dj) % self.size
                if self.grid[ni, nj].state != 0:
                    density += (self.grid[ni, nj].state * 100)
        return density

    def neighbours(self, i, j, radius, states=[1,2,3]):
        """
        Returns a list of neighbours in a given radius around a positio

        :param i: Vertical position of the agent
        :param j: Horizontal position of the agent
        :param radius: Radius around the agent
        :param states: States of the neighbours
        :return: Neighbours in a given radius around a position in a given state
        """
        # List with neighbours
        neighbour_list = []

        # Get neighbors
        for di in range(-radius, radius + 1):
            for dj in range(-radius, radius + 1):
                # Skip the current cell
                if di == 0 and dj == 0:
                    continue

                # Ensure we wrap around the grid boundaries
                ni, nj = (i + di) % self.size, (j + dj) % self.size

                # Get neighbor
                neighbour = self.grid[ni, nj]

                # Check if neighbor is in state
                if neighbour.state in states:
                    neighbour_list.append(neighbour)

        return neighbour_list

    def update(self, frame):
        """
        Update the grid

        :param frame: Current frame
        :return: States of each agent in the grid
        """
        # Get densities
        densities = density_grid(self.get_grid_states())

        # Create a new grid
        newGrid = np.copy(self.grid)

        # Loop through each agent
        for i in range(self.size):
            for j in range(self.size):
                # Get agent
                agent = self.grid[i, j]
                agent.position = (i, j)

                # If agent is not in state 0 nor 4
                if agent.state == 1 or agent.state == 2 or agent.state == 3:
                    # Determine direction to move
                    direction = agent.move(i, j, densities, self.grid)
                    if direction:
                        new_i, new_j = direction

                        # Swap agents if the new position is in state 0
                        if newGrid[new_i, new_j].state == 0:
                            newGrid[new_i, new_j], newGrid[i, j] = newGrid[i, j], newGrid[new_i, new_j]
                            agent.position = (new_i, new_j)

                # If agent is dissipating
                if agent.state == 4:
                    direction = agent.dissipate(i, j, self.size)
                    new_i, new_j = direction

                    # Update position
                    newGrid[new_i, new_j], newGrid[i, j] = newGrid[i, j], newGrid[new_i, new_j]
                    agent.position = (new_i, new_j)

                    # Update dissipation days and state
                    agent.days_dissipate += 1
                    if agent.days_dissipate >= 5:
                        agent.days_dissipate = 0
                        agent.state = 1



        # Update grid
        self.grid = newGrid

        # Check if any agents are next to each other
        for i in range(self.size):
            for j in range(self.size):
                agent = self.grid[i, j]

                # If agent is in state 1
                if agent.state == 1:
                    # Get neighbours
                    neighbours = self.neighbours(i, j, 3, [1])
                    if len(neighbours) > self.proto_size:
                        # Create new group
                        new_group = Group(agent, self.star_size, self.star, self.dissipation)
                        for neighboursAgent in neighbours:
                            if neighboursAgent.state == 1:
                                new_group.append(neighboursAgent)

                        # Add group to list
                        self.groups.append(new_group)
                        continue

                    # If agent is next to an agent in state 2
                    neighbours = self.neighbours(i, j, 1, [2])
                    if len(neighbours) > 0:
                        for neighbour in neighbours:
                            if neighbour.group:
                                neighbour.group.append(agent)
                                break
                        continue


                    # If next to an agent in state 3
                    neighbours = self.neighbours(i, j, 1, [3])
                    if len(neighbours) > 0:
                        for neighbour in neighbours:
                            if neighbour.group:
                                neighbour.group.append(agent)
                                break
                        continue

                # Check for merging groups
                elif agent.state == 2 or agent.state == 3:
                    neighbours = self.neighbours(i, j, 1, [2, 3])
                    if len(neighbours) > 0:
                        for neighbour in neighbours:
                            # Both agents have a group
                            if agent.group and neighbour.group:
                                # If they are not in the same group
                                if neighbour.group != agent.group and neighbour.group:
                                    # Merge lower state group into higher state group
                                    if neighbour.state > agent.state:
                                        neighbour.group.merge(agent.group)
                                    else:
                                        agent.group.merge(neighbour.group)
                        continue

        # Storing groups that are not deleted
        updated_groups = []

        # Looping through each group
        for group in self.groups:
            # Check if group has been merged into another group
            if group.merged:
                del group
                continue

            # Check if still a star
            is_star = group.update()
            if is_star:
                updated_groups.append(group)


            # Is dissipating
            else:
                del group

        # Update groups
        self.groups = updated_groups
        return self.get_grid_states()


    def get_grid_states(self):
        """
        Returns the state of each agent in the grid

        :return: State of agents
        """
        return np.array([[agent.state for agent in row] for row in self.grid])

