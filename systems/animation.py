# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Filename:    animation.py
# Created:     03/16/2017
# Author:      TurBoss
# E-mail:      j.l.toledano.l@gmail.com
# License:     GNU GPL 3.0
# ---------------------------------------------------------------------------

from sdl2.ext import Applicator

from const import WindowSize

from components.spritesheet import SpriteSheet
from components.frames import Frames
from components.motion import MotionType
from components.facing import Facing


class PlayerAnimationSystem(Applicator):
    def __init__(self, player):
        super(PlayerAnimationSystem, self).__init__()
        self.componenttypes = Frames, MotionType, Facing

        self.player = player

        self.sprite_sheet = SpriteSheet()

        self.motion_type = "standing"
        self.facing = "down"
        self.last_facing = self.facing
        self.last_motion_type = self.motion_type

    def process(self, world, componentsets):
        for frames, motion_type, facing in componentsets:

            self.facing = facing.get()
            self.motion_type = motion_type.get()

            if (self.facing != self.last_facing) or (self.motion_type != self.last_motion_type):
                frames.set(0)

            if frames.get() == self.sprite_sheet.get_sprite_sheet_width(self.motion_type) / 128:
                frames.set(0)

            self.last_facing = self.facing
            self.last_motion_type = self.motion_type

            self.player.sprite = self.sprite_sheet.get_sprite(frames.get(), motion_type.get(), facing.get())
            self.player.sprite.position = int(WindowSize.WIDTH / 2) - 64, int(WindowSize.HEIGHT / 2) - 64

            frames.bump()
