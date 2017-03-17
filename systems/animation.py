# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Filename:    animation.py
# Created:     03/16/2017
# Author:      TurBoss
# E-mail:      j.l.toledano.l@gmail.com
# License:     GNU GPL 3.0
# ---------------------------------------------------------------------------

from sdl2.ext import Applicator, SoftwareSprite

from components.frames import Frames


class AnimationSystem(Applicator):
    def __init__(self, motion_type, facing, sprite_size):
        super(AnimationSystem, self).__init__()
        self.componenttypes = (Frames, SoftwareSprite)

        self.motion_type = motion_type
        self.last_motion_type = self.motion_type

        self.facing = facing
        self.last_facing = self.facing

        self.sprite_size = sprite_size

    def process(self, world, componentsets):
        for frames, sprite in componentsets:

            if (self.facing != self.last_facing) or (self.motion_type != self.last_motion_type):
                frames.set_frame(0)

            if frames.get_frame() == sprite.size[0] / self.sprite_size[0]:
                frames.set_frame(0)

            self.last_facing = self.facing
            self.last_motion_type = self.motion_type

            sprite_crop = (frames.get_frame() * self.sprite_size[0],
                           self.facing * self.sprite_size[1],
                           self.sprite_size[0],
                           self.sprite_size[1])

            sprite = sprite.subsprite(sprite_crop)

            frames.bump_frame()
