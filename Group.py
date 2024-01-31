import numpy as np
from group_monitor import GroupMonitor

class Group:
    """
    Class representing a group of agents

    Attributes
    ----------
    agents : list
        List of agents in the group
    star_size : int
        Size of the group before it becomes a star
    size : int
        Size of the group
    steps : int
        Counter used to determine when transitions happen
    star : int
        Time needed for a proto-star to become a star
    dissipation : int
        Time needed for a star to dissipate
    state : int
        State of the group

    Methods
    -------
    append(agent)
        Appends an agent to the group
    calculate_center()
        Calculates the center of the group
    update()
        Updates the group

    """
    def __init__(self, agent, star_size, star, dissipation):
        """
        Constructs a new group

        :param agent: Agent to be added to the group
        :param star_size: Size of the group before it becomes a star
        :param star: Time needed for a proto-star to become a star
        :param dissipation: Time needed for a star to dissipate
        """
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
        self.id = None
        self.group_monitor = GroupMonitor()

    def append(self, agent):
        """
        Appends an agent to the group

        :param agent: Agent to be added to the group
        """
        self.agents.append(agent)
        self.size += 1
        agent.state = self.state
        agent.group = self

    def calculate_center(self):
        """
        Calculates the center of the group

        :return: Center of the group
        """
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
    

    def calculate_distance(center1, center2):
        """
        Calculate Euclidean distance between two centers.

        """
        return np.sqrt((center1[0] - center2[0])**2 + (center1[1] - center2[1])**2)



    def update(self, group_monitor):
        """
        Updates the group.

        :param group_monitor: An instance of Group_monitor to check distances between groups
        :return: boolean indicating if the group has dissipated
        """
        # Check which state the group is in
        if self.state == 2:
            # Update the group's center in the monitor
            self.group_monitor.update_group(self)

            # Check for proximity with other groups in state 2
            for other_id, other_center in self.group_monitor.group_dict.items():
                if other_id != self.id:
                    distance = self.calculate_distance(self.calculate_center(), other_center)
                    if distance < 30:
                        other_group = self.group_monitor.get_group(other_id)
                        if other_group and other_group.steps >= other_group.star and other_group.size >= other_group.star_size:
                            self.state = 3
                            other_group.state = 3
                            for agent in self.agents:
                                agent.state = self.state
                            for agent in other_group.agents:
                                agent.state = other_group.state
                            self.steps = 0
                            other_group.steps = 0
                            # Assuming you remove groups from monitor when state changes from 2
                            self.group_monitor.remove_group(self)
                            self.group_monitor.remove_group(other_group)
                            break  # Assuming merge with one group at a time


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
        return False

