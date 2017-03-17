class Frames:
    def __init__(self):
        super(Frames, self).__init__()
        self.frame = 0

    def get_frame(self):
        return self.frame

    def set_frame(self, frame):
        self.frame = frame

    def bump_frame(self):
        self.frame += 1
