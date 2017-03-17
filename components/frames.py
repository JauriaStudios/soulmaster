class Frames:
    def __init__(self):
        super(Frames, self).__init__()
        self.frame = 0

    def get(self):
        return self.frame

    def set(self, frame):
        self.frame = frame

    def bump(self):
        self.frame += 1
