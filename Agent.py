import numpy as np

class Agent:
    def __init__(self, state):
        self.state = state
        self.group = None
        self.position = None
        self.steps_proto = 0
        self.steps_star = 0
        self.steps_dissipating = 0 
        self.center_group = None       

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