# -*- coding: utf-8 -*-

import json

from sdl2 import SDL_Rect, SDL_RenderCopy
from sdl2.ext import Resources, SpriteFactory, TEXTURE

from const import WindowSize, Colors
from utils import Timer, dice
from db import DataBase
from ui import Dialog

RESOURCES = Resources(__file__, 'resources')


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


class NPC:
    def __init__(self, window, renderer, json_data):

        self.dialog_timer = Timer(10000, activated=True)
        self.close_dialog_timer = Timer(10000)

        self.db = DataBase()

        self.window = window
        self.renderer = renderer

        data = json.loads(json_data)

        self.name = data["name"]
        self.start_pos = data["start_pos"]

        self.npc_data = self.db.get_npc(self.name)

        self.level = self.npc_data["level"]
        self.quest = self.npc_data["quest"]
        self.sprite_size = 128
        self.position = [0, 0]
        self.movement = [0, 0]

        self.moving = False

        self.npc_sprites = [
            RESOURCES.get_path("{0}_standing.png".format(self.name)),
            RESOURCES.get_path("{0}_walking.png".format(self.name))
        ]

        self.factory = SpriteFactory(
            TEXTURE,
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
        self.dialog_box = None
        self.msg = None

    def init_sprite_sheet(self):
        for motion_type in range(MotionType.COUNT):
            self.load_image(self.npc_sprites[motion_type], motion_type)

    def load_image(self, file_path, motion_type):
        sprite_sheets = self.sprite_sheets.get(file_path)
        if not sprite_sheets:
            sprite_surface = self.factory.from_image(file_path)
            self.sprite_sheets[motion_type] = sprite_surface

    def update(self, position, elapsed_time):

        self.position = position

        self.frame_index += 1

        if self.frame_index == (self.sprite_sheets[self.motion_type].size[0] / self.sprite_size):
            self.frame_index = 0

        if not self.moving:
            move = dice(200)
            if move[0] == 200:
                self.moving = True
                self.walk_frames = 60
                facing = dice(Facing.COUNT - 1)
                self.facing = facing[0]

        if self.moving:
            if self.walk_frames:
                self.motion_type = MotionType.WALKING

                if self.facing == 0:
                    # print("LEFT_DOWN")
                    self.movement[0] -= 2
                    self.movement[1] += 1
                    self.facing = Facing.LEFT_DOWN
                elif self.facing == 1:
                    # print("DOWN")
                    self.movement[1] += 1
                    self.facing = Facing.DOWN
                elif self.facing == 2:
                    # print("RIGHT_DOWN")
                    self.movement[0] += 2
                    self.movement[1] += 1
                    self.facing = Facing.RIGHT_DOWN
                elif self.facing == 3:
                    # print("RIGHT")
                    self.movement[0] += 2
                    self.facing = Facing.RIGHT
                elif self.facing == 4:
                    # print("RIGHT_UP")
                    self.movement[0] += 2
                    self.movement[1] -= 1
                    self.facing = Facing.RIGHT_UP
                elif self.facing == 5:
                    # print("UP")
                    self.movement[1] -= 1
                    self.facing = Facing.UP
                elif self.facing == 6:
                    # print("LEFT_UP")
                    self.movement[0] -= 2
                    self.movement[1] -= 1
                    self.facing = Facing.LEFT_UP
                elif self.facing == 7:
                    # print("LEFT")
                    self.movement[0] -= 2
                    self.facing = Facing.LEFT

                self.walk_frames -= 1
            else:
                self.moving = False
                self.motion_type = MotionType.STANDING

        self.dialog_update()

    def draw(self):

        renderer = self.renderer.renderer
        motion_type = self.motion_type
        facing = self.facing
        frame_index = self.frame_index
        position = self.position
        movement = self.movement

        sprite = self.sprite_sheets[motion_type]
        sprite_size = self.sprite_size

        x = int((int(self.start_pos[0]) + position[0] + movement[0]) - (sprite_size / 2))
        y = int((int(self.start_pos[1]) + position[1] + movement[1]) - (sprite_size / 2))

        src_rect = SDL_Rect()

        src_rect.x = frame_index * sprite_size
        src_rect.y = facing * sprite_size
        src_rect.w = sprite_size
        src_rect.h = sprite_size

        dest_rect = SDL_Rect()

        dest_rect.x = x
        dest_rect.y = y
        dest_rect.w = sprite_size
        dest_rect.h = sprite_size

        SDL_RenderCopy(renderer, sprite.texture, src_rect, dest_rect)

        self.dialog_draw((x, y))

    def dialog_update(self):

        self.dialog_timer.update()

        if self.dialog_timer.check():
            self.dialog_timer.reset()
            self.close_dialog_timer.activate()
            self.msg = dice(len(self.dialogs) - 1)
            self.dialog_box = Dialog(self.window, self.renderer, Colors.WHITE, 16, (10, 400), Colors.BLACK)

        self.close_dialog_timer.update()

        if self.close_dialog_timer.check():
            self.close_dialog_timer.reset()
            self.dialog_timer.activate()
            self.dialog_box = None

    def dialog_draw(self, position):

        if self.dialog_box:

            x, y = position

            name = self.dialogs[self.msg[0]]['npc']
            text = self.dialogs[self.msg[0]]['text']
            message = {0: "{0}:".format(name)}

            max_chars = 24
            i = 1
            for j in range(0, len(text), max_chars):
                message[i] = text[j:j+max_chars]
                i += 1

            self.dialog_box.draw(message, (x, y - 100))
