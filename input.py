# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Filename:    input.py
# Created:     03/16/2017
# Author:      TurBoss
# E-mail:      j.l.toledano.l@gmail.com
# License:     GNU GPL 3.0
# ---------------------------------------------------------------------------

""" Handles input """

from collections import defaultdict


class Input:
    def __init__(self):
        self.held_keys = defaultdict(bool)
        self.pressed_keys = defaultdict(bool)
        self.released_keys = defaultdict(bool)

    def begin_new_frame(self):
        self.pressed_keys.clear()
        self.released_keys.clear()

    def key_down_event(self, event):
        self.pressed_keys[event.key.keysym.sym] = True
        self.held_keys[event.key.keysym.sym] = True

    def key_up_event(self, event):
        self.released_keys[event.key.keysym.sym] = True
        self.held_keys[event.key.keysym.sym] = False

    def was_key_pressed(self, key):
        return self.pressed_keys[key]

    def was_key_released(self, key):
        return self.released_keys[key]

    def is_key_held(self, key):
        return self.held_keys[key]
