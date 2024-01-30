import numpy as np
import math

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
    

    def dissipate(self, pos_c_i, pos_c_j, pos_agent_i, pos_agent_j, size):

        vec_i = pos_c_i - pos_agent_i
        vec_j = pos_c_j - pos_agent_j
        angle = 0

        if vec_i != 0 and vec_j != 0:

            angle = math.degrees(math.atan(vec_j/vec_i))
            print(angle)
            
        elif vec_i == 0:

            if pos_agent_j > pos_c_j:

                return pos_agent_i, (pos_agent_j + 1) % size
            
            elif pos_agent_j < pos_c_j:
                
                return pos_agent_i, (pos_agent_j - 1) % size
        
        elif vec_j == 0:

            if pos_agent_i > pos_c_i:

                return (pos_agent_i - 1) % size, pos_agent_j
            
            elif pos_agent_i > pos_c_i:

                return (pos_agent_i + 1) % size, pos_agent_j


        if  angle >= 337.5 or angle < 22.5:
            return (pos_agent_i - 1) % size, pos_agent_j
        elif angle >= 22.5 and angle < 67.5:
            return (pos_agent_i - 1) % size, (pos_agent_j + 1) % size
        elif angle >= 67.5 and angle < 112.5:
            return pos_agent_i, (pos_agent_j + 1) % size
        elif angle >= 112.5 and angle < 157.5:
            return (pos_agent_i + 1) % size, (pos_agent_j + 1) % size
        elif angle >= 157.5 and angle < 202.5:
            return (pos_agent_i + 1) % size, pos_agent_j
        elif angle >= 202.5 and angle < 247.5:
            return (pos_agent_i + 1) % size, (pos_agent_j - 1) % size
        elif angle >= 247.5 and angle < 292.5:
            return pos_agent_i, (pos_agent_j - 1) % size
        elif angle >= 292.5 and angle < 337.5:
            return (pos_agent_i - 1) % size, (pos_agent_j - 1) % size
        else:
            return pos_agent_i, pos_agent_j



