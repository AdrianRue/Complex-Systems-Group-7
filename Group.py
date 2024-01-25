import numpy as np


class Group:
    def __init__(self, agent, key):
        self.agents = [agent]
        self.size = 1
        self.key = key

    def __add__(self, group):
        self.agents += group.agents
        self.size += group.size

    def append(self, agent):
        self.agents.append(agent)
        self.size += 1

    def move(self, direction, size):
        # Change in positions
        positionChange = []

        # Loop through agents
        for agent in self.agents:
            # Position
            position = agent.position

            # Calculate new position
            newPosition = np.add(position, direction)

            # Check if agent is out of bounds
            inBound = True
            for i in range(2):
                if newPosition[i] < 0 or newPosition[i] >= size:
                    inBound = False
                    break

            # Update position
            if inBound:
                agent.position = tuple(newPosition)
                positionChange.append((position, agent.position))

        return positionChange
