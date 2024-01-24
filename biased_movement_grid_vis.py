import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random

class Agent:
    def __init__(self, state, x, y, grid, grid_size, visibility_range=2):
        self.state = state
        self.x = x
        self.y = y
        self.grid = grid
        self.grid_size = grid_size
        self.visibility_range = visibility_range

    def move(self):
        ''' Move towards the direction with the highest density of particles within the visibility range '''
        directions = {'up': (0, -1), 'down': (0, 1), 'left': (-1, 0), 'right': (1, 0)}
        density = {dir: self.calculate_density(dir_vec) for dir, dir_vec in directions.items()}
        # Choose the direction with the highest density
        max_density_direction = max(density, key=density.get)
        return max_density_direction

    def calculate_density(self, direction_vector):
        ''' Calculate the density of particles in a given direction within the visibility range '''
        density = 0
        for i in range(1, self.visibility_range + 1):
            check_x = self.x + direction_vector[0] * i
            check_y = self.y + direction_vector[1] * i
            # Check if the position is within the grid bounds
            if 0 <= check_x < self.grid_size and 0 <= check_y < self.grid_size:
                if self.grid[check_x][check_y].state != 0:
                    density += 1
        return density

class CellularAutomaton:
    def __init__(self, size, agent_probs, visibility_range=2):
        self.size = size
        self.visibility_range = visibility_range
        self.grid = [[Agent(state, x, y, self.grid, size, visibility_range) for y, state in enumerate(row)] for x, row in enumerate(np.random.choice([0, 1], size*size, p=agent_probs).reshape(size, size))]

    def update(self, frame):
        new_grid = np.copy(self.grid)
        for i in range(self.size):
            for j in range(self.size):
                agent = self.grid[i][j]
                if agent.state != 0:  # Only move agents that are not in state 0
                    direction = agent.move()
                    # Calculate new position based on direction
                    dx, dy = {'up': (0, -1), 'down': (0, 1), 'left': (-1, 0), 'right': (1, 0)}[direction]
                    new_x, new_y = agent.x + dx, agent.y + dy
                    # Check if new position is within grid bounds
                    if 0 <= new_x < self.size and 0 <= new_y < self.size:
                        # Move agent to new position in new_grid
                        new_grid[new_x][new_y], new_grid[agent.x][agent.y] = new_grid[agent.x][agent.y], new_grid[new_x][new_y]
        self.grid = new_grid

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

ani = animation.FuncAnimation(fig, update, interval=10, save_count=50)
plt.show()