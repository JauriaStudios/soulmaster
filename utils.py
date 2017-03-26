# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Filename:    utils.py
# Created:     03/16/2017
# Author:      TurBoss
# E-mail:      j.l.toledano.l@gmail.com
# License:     GNU GPL 3.0
# ---------------------------------------------------------------------------

""" Game utulities"""

from random import randrange

from sdl2 import SDL_GetTicks


def count_chars(text):
    """ Count characters in a dictionary of strings"""
    chars = []
    i = 0
    for k, v in text.items():
        i += 1
        j = 0
        for _ in v:
            j += 1
        chars.append(j)

    return i, max(chars)


def int_map(x, in_min, in_max, out_min, out_max):
    """ maps a int range to another range """
    return (x - in_min) * (out_max - out_min) // (in_max - in_min) + out_min


def dict_factory(cursor, row):
    """ Creates dictionaries from sqlite queries """
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def dice(dice_faces, num=1):
    """ Random numbers """
    results = []
    for i in range(num):
        result = randrange(0, dice_faces)
        results.append(result)

    return results


class Timer:
    """ Timer """
    def __init__(self, ticks, activated=False):
        """ Initialize the timer """
        self.start_ticks = 0
        self.current_ticks = 0
        self.previous_ticks = 0
        self.interval = ticks
        self.enabled = False
        self.activated = activated

    def update(self):
        """ Update the timer"""
        if self.activated:
            self.current_ticks = SDL_GetTicks()
            # self.current_ticks -= self.start_ticks
            if self.current_ticks - self.previous_ticks >= self.interval:
                self.previous_ticks = self.current_ticks
                self.enabled = True

    def check(self):
        """ Check if timer reached its limit """
        return self.enabled

    def reset(self):
        """ Resets the timer """
        self.activated = False
        self.enabled = False

    def activate(self):
        """ Activates the timer """
        self.start_ticks = SDL_GetTicks()
        self.activated = True
