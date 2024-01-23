import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random


class Agent:
    def __init__(self, state):
        self.state = state

    def move(self):
        '''
        Here is where we put the rules.
        Right now it's simply: randomly choose a direction to move
        '''
        return random.choice(['up', 'down', 'left', 'right'])


class CellularAutomaton:
    def __init__(self, size, agent_probs):
        self.size = size
        self.grid = np.array([[Agent(state) for state in row] for row in np.random.choice([0, 1, 2, 3], size*size, p=agent_probs).reshape(size, size)])

    def update(self, frame):
        newGrid = np.copy(self.grid)
        for i in range(self.size):
            for j in range(self.size):
                agent = self.grid[i, j]
                if agent.state != 0:  # Only move agents that are not in state 0
                    direction = agent.move()
                    # Determine new position based on direction
                    if direction == 'up':
                        new_i, new_j = (i-1) % self.size, j
                    elif direction == 'down':
                        new_i, new_j = (i+1) % self.size, j
                    elif direction == 'left':
                        new_i, new_j = i, (j-1) % self.size
                    else:  # 'right'
                        new_i, new_j = i, (j+1) % self.size

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
automaton = CellularAutomaton(N, [0.85, 0.05, 0.05, 0.05])

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
