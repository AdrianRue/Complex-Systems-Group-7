import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.colors as mcolors

from Group import Group
from Agent import Agent


class CellularAutomaton:
    def __init__(self, size, agent_probs, star_ts=10, diss_ts=30):
        self.size = size
        self.grid = np.array([[Agent(state) for state in row] for row in np.random.choice([0, 1], size*size, p=agent_probs).reshape(size, size)], dtype=Agent)
        self.groups = []
        self.star = star_ts
        self.dissipation = diss_ts

    def get_density(self, i, j, radius=3):
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


    def count_state1_in_region(self, i, j, radius=4):
        count = 0
        for di in range(-radius, radius + 1):
            for dj in range(-radius, radius + 1):
                # Skip the current cell
                if di == 0 and dj == 0:
                    continue
                # Ensure we wrap around the grid boundaries
                ni, nj = (i + di) % self.size, (j + dj) % self.size
                if self.grid[ni, nj].state == 1:
                    count += 1
        return count


    def update(self, frame):
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
                    if len(neighbours) > 35:
                        # Create new group
                        new_group = Group(agent, self.star, self.dissipation)
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


                # elif agent.state == 4:
                #
                #     if agent.steps_dissipating < 10:
                #         direction = self.dissipate(self.get_density, i, j, self.size)
                #         new_i, new_j = direction
                #
                #         if newGrid[new_i, new_j].state == 0:
                #             newGrid[new_i, new_j], newGrid[i, j] = newGrid[i, j], newGrid[new_i, new_j]
                #
                #         agent.steps_dissipating += 1
                #     else:
                #         agent.state = 1
                #         agent.steps_dissipating = 0

        # Update groups
        remove_groups = []
        # print(len(self.groups))
        for i in range(len(self.groups)):
            dissipation = self.groups[i].update()
            if dissipation:
                remove_groups.append(i)

        # Remove from groups
        for index in remove_groups:
            self.groups.pop(index)
        # print(len(self.groups))

        return self.get_grid_states()


    def get_grid_states(self):
        return np.array([[agent.state for agent in row] for row in self.grid])


def simulate(N, prob_gas):
    p = [1-prob_gas, prob_gas]

    # Initialize the cellular automaton
    automaton = CellularAutomaton(N, p)

    # Define colors for each state
    colors = {0: 'white',  # Color for state 0
            1: 'blue',   # Color for state 1
            2: 'red',    # Color for state 2
            3: 'green'}  # Color for state 3

    # Create a color map from the defined colors
    cmap = mcolors.ListedColormap([colors[i] for i in range(len(colors))])

    # Set up the figure for visualization
    fig, ax = plt.subplots()
    mat = ax.matshow(automaton.get_grid_states(), cmap=cmap, vmin=0, vmax=len(colors))

    # Update function for the animation
    def update(frame):
        mat.set_data(automaton.update(frame))
        return [mat]

    ani = animation.FuncAnimation(fig, update, interval=1/120, save_count=50)
    plt.show()


if __name__ == "__main__":
    simulate(100, 0.15)