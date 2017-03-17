# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Filename:    const.py
# Created:     03/16/2017
# Author:      TurBoss
# E-mail:      j.l.toledano.l@gmail.com
# License:     GNU GPL 3.0
# ---------------------------------------------------------------------------

""" Constants """

from sdl2 import SDL_Color


class WindowSize:
    """ Window width and height """

    WIDTH = 1024
    HEIGHT = 768


class Colors:
    """ Map colors"""

    WHITE = SDL_Color(255, 255, 255)
    BLACK = SDL_Color(0, 0, 0)

    RED = SDL_Color(255, 0, 0)
    GREEN = SDL_Color(0, 255, 0)
    BLUE = SDL_Color(0, 0, 255)
