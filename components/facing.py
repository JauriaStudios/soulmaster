class Facing:
    def __init__(self):
        super(Facing, self).__init__()
        self.facing_types = {"left_down": 0,
                             "down": 1,
                             "right_down": 2,
                             "right": 3,
                             "right_up": 4,
                             "up": 5,
                             "left_up": 6,
                             "left": 7}

        self.facing = self.facing_types["down"]

    def get(self):
        return self.facing

    def get_all(self):
        return self.facing

    def set(self, facing):
        self.facing = self.facing_types[facing]
