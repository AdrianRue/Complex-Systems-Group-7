import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from Group import Group


class Agent:
    def __init__(self, state):
        self.state = state
        self.group = None
        self.position = None

    def move(self, get_density_func, i, j, size):
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

        # Compute sum of densities
        density_sum = sum(densities.values())

        # Density has to be non-zero
        if density_sum != 0:
            # Compute probabilities for each direction
            probabilities = [density / density_sum for density in densities.values()]

            # Choose direction based on probabilities
            direction = np.random.choice(list(directions.keys()), p=probabilities)

        # If density is zero, choose random direction
        else:
            direction = np.random.choice(list(directions.keys()))

        return directions[direction]


class CellularAutomaton:
    def __init__(self, size, agent_probs):
        self.size = size
        self.grid = np.array([[Agent(state) for state in row] for row in np.random.choice([0, 1], size*size, p=agent_probs).reshape(size, size)], dtype=Agent)
        self.groups = {}

    def get_density(self, i, j, radius=3):
        density = 0
        for di in range(-radius, radius + 1):
            for dj in range(-radius, radius + 1):
                if di == 0 and dj == 0:
                    continue  # Skip the current cell

                # If outside the grid go to next
                if i + di < 0 or i + di >= self.size or j + dj < 0 or j + dj >= self.size:
                    continue

                if self.grid[i + di, j + dj].state != 0:
                    density += 1 / (di**2 + dj**2)
        return density

    def neighbours(self, i, j):
        # List with neighbours
        neighbour_list = []

        # Get neighbors
        for di in range(-1, 2):
            # Outside the grid
            if i + di < 0 or i + di == self.size:
                continue
            for dj in range(-1, 2):
                # Outside the grid
                if j + dj < 0 or j + dj == self.size:
                    continue

                # Skip the current cell
                if di == 0 and dj == 0:
                    continue

                # Skip diagonal cells
                if di != 0 and dj != 0:
                    continue

                # Neighbor position
                ni, nj = i + di, j + dj

                # Get neighbor
                neighbour = self.grid[ni, nj]

                # Check if neighbor is in state
                if neighbour.state != 0:
                    neighbour_list.append((neighbour, (ni, nj)))

        return neighbour_list


    def count_state2_in_region(self, i, j, radius=3):
        count = 0
        for di in range(-radius, radius + 1):
            for dj in range(-radius, radius + 1):
                # Skip the current cell
                if di == 0 and dj == 0:
                    continue
                # Ensure we wrap around the grid boundaries
                ni, nj = (i + di) % self.size, (j + dj) % self.size
                if self.grid[ni, nj].state == 2:
                    count += 1
        return count


    def update(self, frame):
        # Moving all agents in state 1
        newGrid = np.copy(self.grid)
        for i in range(self.size):
            for j in range(self.size):
                agent = self.grid[i, j]
                agent.position = (i, j)
                if agent.state == 1:  # Only move agents that are in state 1
                    # Determine direction to move
                    direction = agent.move(self.get_density, i, j, self.size)
                    new_i, new_j = direction

                    # Swap agents if the new position is in state 0
                    if newGrid[new_i, new_j].state == 0:
                        newGrid[new_i, new_j], newGrid[i, j] = newGrid[i, j], newGrid[new_i, new_j]
                        agent.position = (new_i, new_j)

        # Update grid
        self.grid = newGrid

        Flag = False
        # Check if any agents are next to each other
        for i in range(self.size):
            for j in range(self.size):
                agent = self.grid[i, j]
                # Only check agents in state 1
                if agent.state == 1:
                    # Check neighbours
                    neighbour = self.neighbours(i, j)
                    if len(neighbour) > 0:
                        newGroup = None
                        # Loop through neighbors
                        for (neighbourAgent, neighbourPosition) in neighbour:
                            # If neighbor is in state 1
                            if neighbourAgent.state == 1:
                                # Create new group
                                if newGroup is None:
                                    # Key for new group
                                    newKey = max(self.groups.keys()) + 1 if len(self.groups.keys()) > 0 else 0
                                    newGroup = Group(agent, newKey)
                                    self.groups[len(self.groups.keys())] = newGroup

                                    # Update state of current agent
                                    # If the count of state 2 in the region is 19, change to state 3
                                    if self.count_state2_in_region(i, j) >= 19:
                                        agent.state = 3
                                        Flag = True
                                    else:
                                        agent.state = 2

                                # Add neighbour to group
                                if Flag:
                                    neighbourAgent.state = 3
                                else:
                                    neighbourAgent.state = 2

                                neighbourAgent.group = newGroup
                                newGroup.append(neighbourAgent)

                    # Go to next agent
                    continue

                # Check neighbors of agents in state 2
                if agent.state == 2:
                    if agent.group is None:
                        agent.state = 1
                        continue

                    # Get neighbors
                    neighbour = self.neighbours(i, j)

                    # Check if any neighbors are in state 1
                    for (neighbourAgent, neighbourPosition) in neighbour:
                        if neighbourAgent.state == 1:
                            # Add neighbor to group
                            if self.count_state2_in_region(i, j) == 19:
                                neighbourAgent.state = 3
                            else:
                                neighbourAgent.state = 2
                            
                            neighbourAgent.group = agent.group
                            agent.group.append(neighbourAgent)

        # # Movement of groups
        # for group in self.groups.values():
        #     # Get density of group
        #     direction = np.random.randint(-1, 2, 2)
        #
        #     # Move group
        #     positions = group.move(direction, self.size)
        #
        #     for (oldPosition, newPosition) in positions:
        #         # Move agent to new position
        #         self.grid[newPosition] = self.grid[oldPosition]

        return self.get_grid_states()


    def get_grid_states(self):
        return np.array([[agent.state / 5 for agent in row] for row in self.grid])


# Grid size
N = 100

# Initialize the cellular automaton
automaton = CellularAutomaton(N, [0.95, 0.05])

# Set up the figure for visualization
fig, ax = plt.subplots()
cmap = plt.cm.gray_r
mat = ax.matshow(automaton.get_grid_states(), cmap=cmap)

# Update function for the animation
def update(frame):
    mat.set_data(automaton.update(frame))
    return [mat]

ani = animation.FuncAnimation(fig, update, interval=500, save_count=50)
plt.show()
