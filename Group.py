class Group:
    def __init__(self, agent, star, dissipation):
        self.agents = [agent]
        self.size = 1
        self.steps = 0
        self.star = star
        self.dissipation = dissipation
        self.state = 2
        agent.state = self.state

    def append(self, agent):
        self.agents.append(agent)
        self.size += 1
        agent.state = self.state
        agent.group = self

    def calculate_center(self):
        total_i = 0
        total_j = 0
        counter = 0
        
        for i in range(len(self.agents)):
            total_i += self.agents[i].position[0]
            total_j += self.agents[i].position[1]

            counter += 1
        
        center_i = total_i / counter
        center_j = total_j / counter

        return round(center_i), round(center_j)


    def update(self):
        # Check which state the group is in
        if self.state == 2:
            # Check if the group is big enough to become a star
            if self.steps >= self.star and self.size >= 200:
                self.state = 3
                for agent in self.agents:
                    agent.state = self.state

        elif self.state == 3:
            # Check if the group is big enough to dissipate
            if self.steps == self.dissipation:
                self.state = 4
                for agent in self.agents:
                    agent.state = self.state
                return True

        # Update steps
        self.steps += 1