import sys
import os
from random import randint

# If we're on Windows, use the included compiled DLLs.
if sys.platform == "win32":
    os.environ["PYSDL2_DLL_PATH"] = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'libs')

from sdl2 import *


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def dice(dice_faces, num=1):
    results = []
    for i in range(num):
        result = randint(0, dice_faces)
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
            self.current_ticks = timer.SDL_GetTicks()
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
        self.start_ticks = timer.SDL_GetTicks()
        self.activated = True
