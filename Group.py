class Group:
    def __init__(self, agent, star_size, star, dissipation):
        assert isinstance(star_size, int) and star_size > 0, "star_size must be a positive integer"
        assert isinstance(star, int) and star_size > 0, "star must be a positive integer"
        assert isinstance(dissipation, int) and star_size > 0, "dissipation must be a positive integer"

        self.agents = [agent]
        self.star_size = star_size
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
            if self.steps >= self.star and self.size >= self.star_size:
                self.state = 3
                for agent in self.agents:
                    agent.state = self.state

        elif self.state == 3:
            # Check if the group is big enough to dissipate
            if self.steps == self.dissipation:
                self.state = 4
                for agent in self.agents:
                    agent.state = self.state
                    agent.center_group = self.calculate_center()
                return True

        # Update steps
        self.steps += 1