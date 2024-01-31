import numpy as np

class GroupMonitor:
    def __init__(self):
        self.group_dict = {}
        self.next_id = 0

    def add_group(self, group):
        group.id = self.next_id  # This line assigns an id to the group
        self.group_dict[group.id] = group.calculate_center()
        self.next_id += 1

    def update_group(self, group):
        if group.id in self.group_dict:
            self.group_dict[group.id] = group.calculate_center()

    def remove_group(self, group):
        if group.id in self.group_dict:
            del self.group_dict[group.id]

    def get_group_center(self, group_id):
        return self.group_dict.get(group_id, None)

    def calculate_distance(center1, center2):
        return np.sqrt((center1[0] - center2[0])**2 + (center1[1] - center2[1])**2)
