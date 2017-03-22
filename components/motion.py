class MotionType:
    def __init__(self):
        super(MotionType, self).__init__()
        self.motion_types = {"standing": 0,
                             "walking": 1,
                             "casting": 2}

        self.motion_type = self.motion_types["standing"]

    def get(self):
        return self.motion_type

    def get_all(self):
        return self.motion_types

    def set(self, motion_type):
        self.motion_type = self.motion_types[motion_type]
