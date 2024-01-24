import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random


class Agent:
    def __init__(self, state):
        self.state = state
        self.group = None

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

        # Choose the direction with the highest density
        max_density_dir = max(densities, key=densities.get)

        return max_density_dir


class CellularAutomaton:
    def __init__(self, size, agent_probs):
        self.size = size
        self.grid = np.array([[Agent(state) for state in row] for row in np.random.choice([0, 1], size*size, p=agent_probs).reshape(size, size)])
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
                    density += 1
        return density

    def has_neighbor(self, i, j, state):
        # Get neighbors
        for di in range(-1, 2):
            for dj in range(-1, 2):
                if di == 0 and dj == 0:
                    continue
                if di != 0 and dj != 0:
                    continue
                # Ensure we wrap around the grid boundaries
                ni, nj = (i + di) % self.size, (j + dj) % self.size

                if self.grid[ni, nj].state == state:
                    return self.grid[ni, nj]
        return None



    def update(self, frame):
        newGrid = np.copy(self.grid)
        for i in range(self.size):
            for j in range(self.size):
                agent = self.grid[i, j]
                if agent.state == 1:  # Only move agents that are in state 1
                    # Check if next to a neighbor in state 1
                    neighbour = self.has_neighbor(i, j, 1)
                    if neighbour is not None:
                        newGrid[i, j].state = 2

                        # Get group number for key
                        key = len(self.groups.keys())
                        newGrid[i, j].group = key
                        self.groups[key] = [(i, j)]
                        continue

                    # Check if next to a neighbor in state 2
                    neighbour = self.has_neighbor(i, j, 2)
                    if neighbour is not None:
                        newGrid[i, j].state = 2
                        newGrid[i, j].group = neighbour.group
                        self.groups[neighbour.group].append((i, j))
                        continue

                    # Determine direction to move
                    direction = agent.move(self.get_density, i, j, self.size)
                    # Determine new position based on direction
                    if direction == 'up':
                        new_i, new_j = (i - 1) % self.size, j
                    elif direction == 'down':
                        new_i, new_j = (i + 1) % self.size, j
                    elif direction == 'left':
                        new_i, new_j = i, (j - 1) % self.size
                    elif direction == 'right':
                        new_i, new_j = i, (j + 1) % self.size
                    elif direction == 'up-left':
                        new_i, new_j = ((i - 1) % self.size, (j - 1) % self.size)
                    elif direction == 'up-right':
                        new_i, new_j = ((i - 1) % self.size, (j + 1) % self.size)
                    elif direction == 'down-left':
                        new_i, new_j = ((i + 1) % self.size, (j - 1) % self.size)
                    else:   #down-right
                        new_i, new_j = ((i + 1) % self.size, (j + 1) % self.size)

                    # Swap agents if the new position is in state 0
                    if newGrid[new_i, new_j].state == 0:
                        newGrid[new_i, new_j], newGrid[i, j] = newGrid[i, j], newGrid[new_i, new_j]

        self.grid = newGrid
        return self.get_grid_states()

    def get_grid_states(self):
        return np.array([[agent.state for agent in row] for row in self.grid])


# Grid size
N = 50

# Initialize the cellular automaton
automaton = CellularAutomaton(N, [0.90, 0.1])

# Set up the figure for visualization
fig, ax = plt.subplots()
cmap = plt.cm.gray_r
mat = ax.matshow(automaton.get_grid_states(), cmap=cmap)

# Update function for the animation
def update(frame):
    mat.set_data(automaton.update(frame))
    return [mat]

ani = animation.FuncAnimation(fig, update, interval=1000, save_count=50)
plt.show()
