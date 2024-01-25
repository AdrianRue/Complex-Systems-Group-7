import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random
import matplotlib.colors as mcolors


class Agent:
    def __init__(self, state):
        self.state = state
        self.group = None
        self.days_proto = 0
        self.days_star = 0
        self.days_dissipating = 0

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
    
    def dissipate(self, get_density_func, i, j, size):

        # This is simply a reverse of the directions to move away from the clump of mass, couldn't think of a better way atm
        directions = {
            'up': ((i + 1) % size, j),
            'down': ((i - 1) % size, j),
            'left': (i, (j + 1) % size),
            'right': (i, (j - 1) % size),
            'up-left': ((i + 1) % size, (j + 1) % size),
            'up-right': ((i + 1) % size, (j - 1) % size),
            'down-left': ((i - 1) % size, (j + 1) % size),
            'down-right': ((i - 1) % size, (j - 1) % size)
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

    # def count_state2_in_region(self, i, j, radius=1):
    #     count = 0
    #     for di in range(-radius, radius + 1):
    #         for dj in range(-radius, radius + 1):
    #             # Skip the current cell
    #             if di == 0 and dj == 0:
    #                 continue
    #             # Ensure we wrap around the grid boundaries
    #             ni, nj = (i + di) % self.size, (j + dj) % self.size
    #             if self.grid[ni, nj].state == 2:
    #                 count += 1
    #     return count

    # def update(self, frame):
        newGrid = np.copy(self.grid)
        for i in range(self.size):
            for j in range(self.size):
                agent = self.grid[i, j]
                if agent.state == 1:    # Only move agents that are in state 1
                    # Check if next to a neighbor in state 1
                    neighbour = self.has_neighbor(i, j, 1)
                    if neighbour is not None:
                        newGrid[i, j].state = 2
                        # If the count of state 2 is 19, change to state 3
                        if self.count_state2_in_region(i, j) == 19:
                            newGrid[i, j].state = 3
                        else:
                            newGrid[i, j].state = 2
                        continue

                    # Check if next to a neighbor in state 2
                    neighbour = self.has_neighbor(i, j, 2)
                    if neighbour is not None:
                        newGrid[i, j].state = 2
                        # If the count of state 2 is 19, change to state 3
                        if self.count_state2_in_region(i, j) == 19:
                            newGrid[i, j].state = 3
                        else:
                            newGrid[i, j].state = 2

                        newGrid[i, j].group = neighbour.group
                        self.groups[neighbour.group].append((i, j))
                        continue
                    
                    # Determine direction to move
                    direction = agent.move(self.get_density, i, j, self.size)
                    new_i, new_j = direction

                    # Swap agents if the new position is in state 0
                    if newGrid[new_i, new_j].state == 0:
                        newGrid[new_i, new_j], newGrid[i, j] = newGrid[i, j], newGrid[new_i, new_j]


                # Process state 2 agents
                elif agent.state == 2:
                    # Check if the count of state 2 agents is 19, change to state 3
                    if self.count_state2_in_region(i, j) == 19:
                        newGrid[i, j].state = 3
                    else:
                        # Determine direction to move
                        direction = agent.move(self.get_density, i, j, self.size)
                        new_i, new_j = direction

                        # Swap agents if the new position is in state 0
                        if newGrid[new_i, new_j].state == 0:
                            newGrid[new_i, new_j], newGrid[i, j] = newGrid[i, j], newGrid[new_i, new_j]

        self.grid = newGrid
        return self.get_grid_states()
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
        newGrid = np.copy(self.grid)
        for i in range(self.size):
            for j in range(self.size):
                agent = self.grid[i, j]
                if agent.state == 1:  # Only move agents that are in state 1
                    # Check if next to a neighbor in state 1
                    neighbour = self.has_neighbor(i, j, 1)
                    if neighbour is not None:
                        # If the count of state 2 in the region is 19, change to state 3
                        if self.count_state2_in_region(i, j) == 19:
                            newGrid[i, j].state = 3
                        else:
                            newGrid[i, j].state = 2

                        # Get group number for key
                        key = len(self.groups.keys())
                        newGrid[i, j].group = key
                        self.groups[key] = [(i, j)]
                        continue

                    # Check if next to a neighbor in state 2
                    neighbour = self.has_neighbor(i, j, 2)
                    if neighbour is not None:
                        # If the count of state 2 in the region is 19, change to state 3
                        if self.count_state2_in_region(i, j) == 19:
                            newGrid[i, j].state = 3
                        else:
                            newGrid[i, j].state = 2
        
                        newGrid[i, j].group = neighbour.group
                        self.groups[neighbour.group].append((i, j))
                        continue

                    # Determine direction to move
                    direction = agent.move(self.get_density, i, j, self.size)
                    new_i, new_j = direction
                    if newGrid[new_i, new_j].state == 0:
                        newGrid[new_i, new_j], newGrid[i, j] = newGrid[i, j], newGrid[new_i, new_j]

                # Process state 2 agents
                elif agent.state == 2:
                    # Check if the count of state 2 in the region is 19, change to state 3
                    if self.count_state2_in_region(i, j) == 19:
                        newGrid[i, j].state = 3
                    
                    direction = agent.move(self.get_density, i, j, self.size)
                    new_i, new_j = direction
                    if newGrid[new_i, new_j].state == 0:
                        newGrid[new_i, new_j], newGrid[i, j] = newGrid[i, j], newGrid[new_i, new_j]

                
                elif agent.state == 3:
                    # Count number of days star has been in proto state
                    agent.days_proto += 1

                    # Transform proto star into star after long enough
                    if agent.days_proto > 10:

                        agent.days_proto = 0
                        agent.state = 4


                elif agent.state == 4:
                    
                    agent.days_star += 1
                    #after a while, star dies out and parts turn into dissipating gas
                    if agent.days_star > 15:
                        
                        agent.days_star = 0
                        agent.state = 5

                elif agent.state == 5:

                    if agent.days_dissipating < 5:
                        direction = agent.dissipate(self.get_density, i, j, self.size)
                        new_i, new_j = direction

                        if newGrid[new_i, new_j].state == 0:
                            newGrid[new_i, new_j], newGrid[i, j] = newGrid[i, j], newGrid[new_i, new_j]

                        agent.days_dissipating += 1
                    else:
                        agent.state = 1
                        agent.days_dissipating = 0

                    
                




                






        self.grid = newGrid
        return self.get_grid_states()


    def get_grid_states(self):
        return np.array([[agent.state * 50 for agent in row] for row in self.grid])


# Grid size
N = 100

# Initialize the cellular automaton
automaton = CellularAutomaton(N, [0.7, 0.3])

# Define colors for each state
colors = {0: 'white',  # Color for state 0
          1: 'blue',   # Color for state 1
          2: 'red',    # Color for state 2
          3: 'green'}  # Color for state 3

# Create a color map from the defined colors
cmap = mcolors.ListedColormap([colors[i] for i in range(len(colors))])

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
