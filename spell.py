# -*- coding: utf-8 -*-

import os
import sys

# If we're on Windows, use the included compiled DLLs.
if sys.platform == "win32":
    os.environ["PYSDL2_DLL_PATH"] = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'libs')

from sdl2 import SDL_Rect, SDL_RenderCopy
from sdl2.ext import Resources, SpriteFactory, TEXTURE

from const import WindowSize
from utils import int_map

RESOURCES = Resources(__file__, 'resources', 'spells')


class Facing:
    LEFT = 0
    LEFT_UP = 1
    UP = 2
    RIGHT_UP = 3
    RIGHT = 4
    RIGHT_DOWN = 5
    DOWN = 6
    LEFT_DOWN = 7
    COUNT = 8


class Spell:
    def __init__(self, renderer, name, player_facing):
        self.renderer = renderer

        self.sprite_size = 64

        self.sprites = RESOURCES.get_path("{0}.png".format(name))

        self.factory = SpriteFactory(
            TEXTURE,
            renderer=self.renderer
        )

        self.sprite_sheet = self.factory.from_image(self.sprites)

        self.facing = int_map(player_facing, 0, 7, 7, 0)
        print(self.facing)
        self.last_facing = self.facing

        self.frame_index = 0
        self.speed = [0, 0]

    def update(self, elapsed_time):

        self.frame_index += 1

        if self.facing == Facing.LEFT_DOWN:
            self.speed[0] -= 2
            self.speed[1] += 1
        elif self.facing == Facing.DOWN:
            self.speed[1] += 1
        elif self.facing == Facing.RIGHT_DOWN:
            self.speed[0] += 2
            self.speed[1] += 1
        elif self.facing == Facing.RIGHT:
            self.speed[0] += 2
        elif self.facing == Facing.RIGHT_UP:
            self.speed[0] += 2
            self.speed[1] -= 1
        elif self.facing == Facing.UP:
            self.speed[1] -= 1
        elif self.facing == Facing.LEFT_UP:
            self.speed[0] -= 2
            self.speed[1] -= 1
        elif self.facing == Facing.LEFT:
            self.speed[0] -= 2

        if self.facing != self.last_facing:
            self.frame_index = 0

        if self.frame_index == (self.sprite_sheet.size[0] / self.sprite_size):
            self.frame_index = 0

        self.last_facing = self.facing

    def draw(self):

        renderer = self.renderer.renderer
        facing = self.facing
        frame_index = self.frame_index
        speed = self.speed

        sprite = self.sprite_sheet
        sprite_size = self.sprite_size

        src_rect = SDL_Rect()

        src_rect.x = frame_index * sprite_size
        src_rect.y = facing * sprite_size
        src_rect.w = sprite_size
        src_rect.h = sprite_size

        dest_rect = SDL_Rect()

        dest_rect.x = int((WindowSize.WIDTH / 2) + speed[0])
        dest_rect.y = int((WindowSize.HEIGHT / 2) + speed[1])
        dest_rect.w = sprite_size
        dest_rect.h = sprite_size

        SDL_RenderCopy(renderer, sprite.texture, src_rect, dest_rect)
