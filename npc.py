# -*- coding: utf-8 -*-

import sys
import os

from random import randint

# If we're on Windows, use the included compiled DLLs.
if sys.platform == "win32":
    os.environ["PYSDL2_DLL_PATH"] = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'libs')

from sdl2 import *
import sdl2.ext

from const import WindowSize, Colors
from db import DataBase
from ui import Dialog

RESOURCES = sdl2.ext.Resources(__file__, 'resources')


class MotionType:
    STANDING = 0
    WALKING = 1
    COUNT = 1


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


class NPC:
    def __init__(self, window, data):

        self.current_ticks = 0
        self.previous_ticks = 0
        self.dialog_interval = 10000

        self.db = DataBase()

        self.window = window
        self.renderer = window.renderer

        self.name = data["name"]
        self.level = data["level"]
        self.quest = data["quest"]
        self.sprite_size = 128
        self.position = [0, 0]
        self.movement = [0, 0]

        self.moving = False

        self.npc_sprites = [
            RESOURCES.get_path("{0}_standing.png".format(self.name)),
            # RESOURCES.get_path("{0}_walking.png".format(self.name))
        ]

        self.factory = sdl2.ext.SpriteFactory(
            sdl2.ext.TEXTURE,
            renderer=self.renderer
        )

        self.sprite_sheets = {}

        self.facing = Facing.LEFT_DOWN
        self.last_facing = self.facing

        self.motion_type = MotionType.STANDING
        self.last_motion_type = self.motion_type

        self.frame_index = 0
        self.walk_frames = 60

        self.init_sprite_sheet()

        self.dialogs = self.db.get_npc_dialog(self.name)

        self.draw_dialog = False

        self.general_talk = False
        self.dialog_box = None

    def init_sprite_sheet(self):
        for motion_type in range(MotionType.COUNT):
            self.load_image(self.npc_sprites[motion_type], motion_type)

    def load_image(self, file_path, motion_type):
        sprite_sheets = self.sprite_sheets.get(file_path)
        if not sprite_sheets:
            sprite_surface = self.factory.from_image(file_path)
            self.sprite_sheets[motion_type] = sprite_surface

    def update(self, position, elapsed_time):

        self.current_ticks = timer.SDL_GetTicks()

        if self.current_ticks - self.previous_ticks >= self.dialog_interval:
            self.previous_ticks = self.current_ticks

            self.draw_dialog = True

            self.dialog_box = Dialog(self.window, Colors.WHITHE, 16, (10, 400), Colors.BLACK)

        self.position = position

        self.frame_index += 1

        if self.frame_index == (self.sprite_sheets[self.motion_type].size[0] / self.sprite_size):
            self.frame_index = 0

        if not self.moving:
            if randint(0, 200) == 200:
                self.moving = True
                self.walk_frames = 60
                self.facing = randint(0, 7)

        if self.moving:
            if self.walk_frames:

                if self.facing == 0:
                    # print("LEFT_DOWN")
                    self.movement[0] -= 2
                    self.movement[1] += 1
                elif self.facing == 1:
                    # print("DOWN")
                    self.movement[1] += 1
                elif self.facing == 2:
                    # print("RIGHT_DOWN")
                    self.movement[0] += 2
                    self.movement[1] += 1
                elif self.facing == 3:
                    # print("RIGHT")
                    self.movement[0] += 2
                elif self.facing == 4:
                    # print("RIGHT_UP")
                    self.movement[0] += 2
                    self.movement[1] -= 1
                elif self.facing == 5:
                    # print("UP")
                    self.movement[1] -= 1
                elif self.facing == 6:
                    # print("LEFT_UP")
                    self.movement[0] -= 2
                    self.movement[1] -= 1
                elif self.facing == 7:
                    # print("LEFT")
                    self.movement[0] -= 2

                self.walk_frames -= 1
            else:
                self.moving = False

    def draw(self):

        if self.draw_dialog:
            self.dialog_box.draw({0: self.dialogs[0]['npc'], 1: self.dialogs[0]['text']})

        renderer = self.renderer.renderer
        motion_type = self.motion_type
        facing = self.facing
        frame_index = self.frame_index
        position = self.position
        movement = self.movement

        sprite = self.sprite_sheets[motion_type]
        sprite_size = self.sprite_size

        src_rect = SDL_Rect()

        src_rect.x = frame_index * sprite_size
        src_rect.y = facing * sprite_size
        src_rect.w = sprite_size
        src_rect.h = sprite_size

        dest_rect = SDL_Rect()

        dest_rect.x = int(((WindowSize.WIDTH / 2) + position[0] + movement[0]) - (sprite_size / 2))
        dest_rect.y = int(((WindowSize.HEIGHT / 2) + position[1] + movement[1]) - (sprite_size / 2))
        dest_rect.w = sprite_size
        dest_rect.h = sprite_size

        render.SDL_RenderCopy(renderer, sprite.texture, src_rect, dest_rect)
