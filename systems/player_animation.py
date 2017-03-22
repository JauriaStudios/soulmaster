# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Filename:    player_animation.py
# Created:     03/16/2017
# Author:      TurBoss
# E-mail:      j.l.toledano.l@gmail.com
# License:     GNU GPL 3.0
# ---------------------------------------------------------------------------

from sdl2 import SDL_BlitSurface, \
    SDL_Rect, \
    SDL_FillRect

from sdl2.ext import Applicator, \
    Sprite

from components.spritesheet import SpriteSheet
from components.frames import Frames
from components.motion import MotionType
from components.facing import Facing

from player import PlayerData


class PlayerAnimationSystem(Applicator):
    def __init__(self, name):
        super(PlayerAnimationSystem, self).__init__()
        self.componenttypes = PlayerData, Frames, MotionType, Facing, Sprite

        self.sprite_sheet = SpriteSheet(name)

        self.motion_type = "standing"
        self.facing = "down"
        self.last_facing = self.facing
        self.last_motion_type = self.motion_type

        self.surface = None
        self.sprite_surface = None

    def process(self, world, componentsets):
        for playerdata, frames, motion_type, facing, sprite in componentsets:

            if not playerdata.life:
                return

            self.facing = facing.get()
            self.motion_type = motion_type.get()

            if (self.facing != self.last_facing) or (self.motion_type != self.last_motion_type):
                frames.set(0)

            if frames.get() == self.sprite_sheet.get_sprite_sheet_width(self.motion_type) / 128:
                frames.set(0)

            self.last_facing = self.facing
            self.last_motion_type = self.motion_type

            self.surface = self.sprite_sheet.get_surface(frames.get(), motion_type.get(), facing.get())
            self.sprite_surface = sprite.surface

            rect = SDL_Rect(0, 0)
            SDL_FillRect(self.sprite_surface, None, 0x000000)
            SDL_BlitSurface(self.surface, None, self.sprite_surface, rect)

            frames.bump()
