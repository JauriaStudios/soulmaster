# -*- coding: utf-8 -*-

import sys
import os

# If we're on Windows, use the included compiled DLLs.
if sys.platform == "win32":
    os.environ["PYSDL2_DLL_PATH"] = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'libs')

from sdl2 import *
import sdl2.ext

from const import WindowSize

RESOURCES = sdl2.ext.Resources(__file__, 'resources')


class MotionType:
    STANDING = 0
    WALKING = 1
    COUNT = 2


class Facing:
    LEFT_DOWN = 0
    DOWN = 1
    RIGHT_DOWN = 2
    RIGHT = 3
    RIGHT_UP = 4
    UP = 5
    LEFT_UP = 6
    LEFT = 7
    COUNT = 8


class Enemy:
    def __init__(self, renderer, name):
        self.renderer = renderer

        self.sprite_size = 192

        self.enemy_sprites = [
            RESOURCES.get_path("{0}_standing.png".format(name)),
            RESOURCES.get_path("{0}_walking.png".format(name))
        ]

        self.factory = sdl2.ext.SpriteFactory(
            sdl2.ext.TEXTURE, renderer=self.renderer)

        self.sprite_sheets = {}
        self.sprites = {}

        self.facing = Facing.LEFT_DOWN
        self.last_facing = self.facing

        self.motion_type = MotionType.STANDING
        self.last_motion_type = self.motion_type

        self.frame_index = 0

        self.init_sprite_sheet()

    def init_sprite_sheet(self):

        for motion_type in range(MotionType.COUNT):

            self.load_image(self.enemy_sprites[motion_type], motion_type)

    def update(self, motion_type, facing, elapsed_time):
        self.motion_type = motion_type
        self.facing = facing

        self.frame_index += 1

        if (self.facing != self.last_facing) or (self.motion_type != self.last_motion_type):
            self.frame_index = 0

        if self.frame_index == (self.sprite_sheets[self.motion_type].size[0] / 64):
            self.frame_index = 0

        self.last_facing = self.facing
        self.last_motion_type = self.motion_type

    def draw(self):

        renderer = self.renderer.renderer
        motion_type = self.motion_type
        facing = self.facing
        frame_index = self.frame_index

        sprite = self.sprite_sheets[motion_type]
        sprite_size = self.sprite_size

        src_rect = SDL_Rect()

        src_rect.x = frame_index * sprite_size
        src_rect.y = facing * sprite_size
        src_rect.w = sprite_size
        src_rect.h = sprite_size

        dest_rect = SDL_Rect()

        dest_rect.x = int((WindowSize.WIDTH / 2) - sprite_size)
        dest_rect.y = int((WindowSize.HEIGHT / 2) - sprite_size)
        dest_rect.w = sprite_size
        dest_rect.h = sprite_size

        render.SDL_RenderCopy(renderer, sprite.texture, src_rect, dest_rect)

    def load_image(self, file_path, motion_type):
        sprite_sheets = self.sprite_sheets.get(file_path)
        if not sprite_sheets:
            sprite_surface = self.factory.from_image(file_path)
            self.sprite_sheets[motion_type] = sprite_surface
