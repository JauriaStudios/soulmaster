# coding=utf-8

from random import randrange

from sdl2 import SDL_GetTicks


def int_map(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) // (in_max - in_min) + out_min


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def dice(dice_faces, num=1):
    results = []
    for i in range(num):
        result = randrange(0, dice_faces)
        results.append(result)

    return results


class Timer:
    def __init__(self, ticks, activated=False):
        self.start_ticks = 0
        self.current_ticks = 0
        self.previous_ticks = 0
        self.interval = ticks
        self.enabled = False
        self.activated = activated

    def update(self):
        if self.activated:
            self.current_ticks = SDL_GetTicks()
            self.current_ticks -= self.start_ticks
            if self.current_ticks - self.previous_ticks >= self.interval:
                self.previous_ticks = self.current_ticks
                self.enabled = True

    def check(self):
        return self.enabled

    def reset(self):
        self.activated = False
        self.enabled = False

    def activate(self):
        self.start_ticks = SDL_GetTicks()
        self.activated = True
