import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random


class Agent:
    def __init__(self, state):
        self.state = state

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

    def get_density(self, i, j, radius=3):
        density = 0
        for di in range(-radius, radius + 1):
            for dj in range(-radius, radius + 1):
                if di == 0 and dj == 0:
                    continue  # Skip the current cell
                # Ensure we wrap around the grid boundaries
                ni, nj = (i + di) % self.size, (j + dj) % self.size
                if self.grid[ni, nj].state != 0:
                    density += 1
        return density

    def update(self, frame):
        newGrid = np.copy(self.grid)
        for i in range(self.size):
            for j in range(self.size):
                agent = self.grid[i, j]
                if agent.state != 0:  # Only move agents that are not in state 0
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
automaton = CellularAutomaton(N, [0.95, 0.05])

# Set up the figure for visualization
fig, ax = plt.subplots()
cmap = plt.cm.gray_r
mat = ax.matshow(automaton.get_grid_states(), cmap=cmap)

# Update function for the animation
def update(frame):
    mat.set_data(automaton.update(frame))
    return [mat]

ani = animation.FuncAnimation(fig, update, interval=250, save_count=50)
plt.show()
