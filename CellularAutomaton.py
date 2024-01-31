import numpy as np
from Group import Group
from Agent import Agent
from group_monitor import GroupMonitor

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
    def __init__(self, size, agent_probs, proto_size, star_size):
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
        assert all(0 <= p <= 1 for p in agent_probs), "Probabilities in agent_probs must be between 0 and 1"

        self.size = size
        self.proto_size = proto_size
        self.star_size = star_size
        self.grid = np.array([[Agent(state) for state in row] for row in np.random.choice([0, 1], size*size, p=agent_probs).reshape(size, size)], dtype=Agent)
        self.groups = []
        self.star = 10
        self.dissipation = 30
        self.group_monitor = GroupMonitor()

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
        # Moving all agents in state 1
        newGrid = np.copy(self.grid)
        for i in range(self.size):
            for j in range(self.size):
                agent = self.grid[i, j]
                agent.position = (i, j)
                if agent.state == 1 or agent.state == 2 or agent.state == 3:  # Only move agents that are in state 1, 2 or 3
                    # Determine direction to move
                    direction = agent.move(self.get_density, i, j, self.size)
                    new_i, new_j = direction

                    # Swap agents if the new position is in state 0
                    if newGrid[new_i, new_j].state == 0:
                        newGrid[new_i, new_j], newGrid[i, j] = newGrid[i, j], newGrid[new_i, new_j]
                        agent.position = (new_i, new_j)

                if agent.state == 4:

                    direction = agent.dissipate(agent.center_group[0], agent.center_group[1], i, j, self.size)
                    new_i, new_j = direction

                    if newGrid[new_i, new_j].state == 0:
                        newGrid[new_i, new_j], newGrid[i, j] = newGrid[i, j], newGrid[new_i, new_j]
                        agent.position = (new_i, new_j)



        # Update grid
        self.grid = newGrid

        # Update groups and monitor as necessary
        for group in self.groups:
            group_updated = group.update(self.group_monitor)
            if group.state == 2:
                # If the group state is 2, add or update it in the monitor
                if group.id not in self.group_monitor.group_dict:
                    self.group_monitor.add_group(group)
                else:
                    self.group_monitor.update_group(group)
            elif group.state != 2:
                # If the group state is no longer 2, remove it from the monitor
                self.group_monitor.remove_group(group)

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

                        self.groups.append(new_group)

                    # If agent is next to an agent in state 2
                    neighbours = self.neighbours(i, j, 1, [2])
                    if len(neighbours) > 2:
                        neighbours[0].group.append(agent)

                    # If next to an agent in state 3
                    neighbours = self.neighbours(i, j, 1, [3])
                    if len(neighbours) > 2:
                        neighbours[0].group.append(agent)


        # # Update groups
        # remove_groups = []
        # # print(len(self.groups))
        # for i in range(len(self.groups)):
        #     dissipation = self.groups[i].update()
        #     if dissipation:
        #         remove_groups.append(i)

        # # Remove from groups
        # for index in remove_groups:
        #     self.groups.pop(index)
        # # print(len(self.groups))

        return self.get_grid_states()


    def get_grid_states(self):
        """
        Returns the state of each agent in the grid

        :return: State of agents
        """
        return np.array([[agent.state for agent in row] for row in self.grid])

