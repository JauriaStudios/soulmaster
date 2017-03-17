# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Filename:    animation.py
# Created:     03/16/2017
# Author:      TurBoss
# E-mail:      j.l.toledano.l@gmail.com
# License:     GNU GPL 3.0
# ---------------------------------------------------------------------------

from sdl2.ext import Applicator, \
    SoftwareSprite

from components.frames import Frames
from components.motion import MotionType
from components.facing import Facing


class AnimationSystem(Applicator):
    def __init__(self):
        super(AnimationSystem, self).__init__()
        self.componenttypes = (Frames, MotionType, Facing, SoftwareSprite)

        self.motion_type = "standing"
        self.facing = "down"
        self.last_facing = self.facing
        self.last_motion_type = self.motion_type

    def process(self, world, componentsets):
        for frames, motion_type, facing, sprite in componentsets:

            self.facing = facing.get()
            self.motion_type = motion_type.get()

            if (self.facing != self.last_facing) or (self.motion_type != self.last_motion_type):
                frames.set(0)

            if frames.get() == sprite.size[0] / 128:
                frames.set(0)

            self.last_facing = self.facing
            self.last_motion_type = self.motion_type

            sprite_crop = (frames.get() * 128,
                           self.facing * 128,
                           128,
                           128)

            sprite.subsprite(sprite_crop)

            frames.bump()
