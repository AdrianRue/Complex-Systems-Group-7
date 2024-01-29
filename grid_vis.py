import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.colors as mcolors

from Group import Group


class Agent:
    def __init__(self, state):
        self.state = state
        self.group = None
        self.position = None
        self.steps_proto = 0
        self.steps_star = 0
        self.steps_dissipating = 0        

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
        # print("Densities:", densities)  # Debug statement

        # Compute sum of densities
        density_sum = sum(densities.values())

        # Density has to be non-zero
        if density_sum != 0:
            # Compute probabilities for each direction
            probabilities = {dir: density / density_sum for dir, density in densities.items()}
            # print("Probabilities:", probabilities)  # Debug statement

            # Choose direction based on probabilities
            direction = np.random.choice(list(directions.keys()), p=list(probabilities.values()))
        else:
            # If density is zero, choose random direction
            direction = np.random.choice(list(directions.keys()))

        # print("Chosen direction:", direction)  # Debug statement
        return directions[direction]
    

    # def dissipate(self, get_density_func, i, j, size):

    #     # This is simply a reverse of the directions to move away from the clump of mass, couldn't think of a better way atm
    #     directions = {
    #         'up': ((i + 1) % size, j),
    #         'down': ((i - 1) % size, j),
    #         'left': (i, (j + 1) % size),
    #         'right': (i, (j - 1) % size),
    #         'up-left': ((i + 1) % size, (j + 1) % size),
    #         'up-right': ((i + 1) % size, (j - 1) % size),
    #         'down-left': ((i - 1) % size, (j + 1) % size),
    #         'down-right': ((i - 1) % size, (j - 1) % size)
    #     }

    #     # Calculate densities for each direction
    #     densities = {dir: get_density_func(pos[0], pos[1]) for dir, pos in directions.items()}

    #     # Compute sum of densities
    #     density_sum = sum(densities.values())

    #     # Density has to be non-zero
    #     if density_sum != 0:
    #         # Compute probabilities for each direction
    #         probabilities = [density / density_sum for density in densities.values()]

    #         # Choose direction based on probabilities
    #         direction = np.random.choice(list(directions.keys()), p=probabilities)

    #     # If density is zero, choose random direction
    #     else:
    #         direction = np.random.choice(list(directions.keys()))

    #     return directions[direction]


class CellularAutomaton:
    def __init__(self, size, agent_probs, star, dissipation):
        self.size = size
        self.grid = np.array([[Agent(state) for state in row] for row in np.random.choice([0, 1], size*size, p=agent_probs).reshape(size, size)], dtype=Agent)
        self.groups = []
        self.star = star
        self.dissipation = dissipation

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
                    density += self.grid[ni, nj].state
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


    def count_state1_in_region(self, i, j, radius=3):
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
                    neighbours = self.neighbours(i, j, 1, [1])
                    if len(neighbours) > 6:
                        # Create new group
                        new_group = Group(agent, self.star, self.dissipation)
                        for neighboursAgent in neighbours:
                            if neighboursAgent.state == 1:
                                new_group.append(neighboursAgent)

                        self.groups.append(new_group)

                    # If agent is next to an agent in state 2
                    neighbours = self.neighbours(i, j, 1, [2])
                    if len(neighbours) > 0:
                        neighbours[0].group.append(agent)

                    # If next to an agent in state 3
                    neighbours = self.neighbours(i, j, 1, [3])
                    if len(neighbours) > 0:
                        neighbours[0].group.append(agent)


                

        # Update groups
        remove_groups = []
        #print(len(self.groups))
        for i in range(len(self.groups)):
            dissipation = self.groups[i].update()
            if dissipation:
                remove_groups.append(i)

        # Remove from groups
        for index in remove_groups:
            self.groups.pop(index)
        #print(len(self.groups))
            

        return self.get_grid_states()


    def get_grid_states(self):
        return np.array([[agent.state for agent in row] for row in self.grid])


# Grid size
N = 100

# Initialize the cellular automaton
automaton = CellularAutomaton(N, [0.9, 0.1], 10,30)

# Define colors for each state
colors = {0: 'white',  # Color for state 0
          1: 'green',   # Color for state 1
          2: 'yellow',    # Color for state 2
          3: 'orange',  #  Color for state 3
          4: 'blue'}  # Color for state 4

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
