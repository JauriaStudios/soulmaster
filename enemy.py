# -*- coding: utf-8 -*-

from sdl2 import SDL_Rect,\
    SDL_RenderCopy
from sdl2.ext import Resources

from const import WindowSize
from utils import dice

RESOURCES = Resources(__file__, 'resources')


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


class Enemy:
    def __init__(self, renderer, factory, name):
        self.renderer = renderer
        self.factory = factory

        self.sprite_size = 128
        self.start_pos = [100, 200]
        self.position = [0, 0]
        self.movement = [0, 0]

        self.moving = False
        self.move_rate = 100

        self.enemy_sprites = [
            RESOURCES.get_path("{0}_standing.png".format(name)),
            # RESOURCES.get_path("{0}_walking.png".format(name))
        ]

        self.sprite_sheets = {}
        self.sprites = []

        self.facing = Facing.LEFT_DOWN
        self.last_facing = self.facing

        self.motion_type = MotionType.STANDING
        self.last_motion_type = self.motion_type

        self.frame_index = 0
        self.walk_frames = 60

        self.init_sprite_sheet()

    def init_sprite_sheet(self):
        for motion_type in range(MotionType.COUNT):
            self.load_image(self.enemy_sprites[motion_type], motion_type)

    def load_image(self, file_path, motion_type):
        sprite_sheets = self.sprite_sheets.get(file_path)
        if not sprite_sheets:
            sprite_surface = self.factory.from_image(file_path)
            self.sprite_sheets[motion_type] = sprite_surface

    def update(self, position, elapsed_time):
        self.sprites.clear()
        self.position = position
        self.frame_index += 1

        if self.frame_index == (self.sprite_sheets[self.motion_type].size[0] / self.sprite_size):
            self.frame_index = 0

        if not self.moving:
            move = dice(self.move_rate)
            if move[0] == self.move_rate - 1:
                self.moving = True
                self.walk_frames = 60
                facing = dice(7)
                self.facing = facing[0]

        if self.moving:
            if self.walk_frames:

                if self.facing == 0:
                    self.movement[0] -= 2
                    self.movement[1] += 1
                elif self.facing == 1:
                    self.movement[1] += 1
                elif self.facing == 2:
                    self.movement[0] += 2
                    self.movement[1] += 1
                elif self.facing == 3:
                    self.movement[0] += 2
                elif self.facing == 4:
                    self.movement[0] += 2
                    self.movement[1] -= 1
                elif self.facing == 5:
                    self.movement[1] -= 1
                elif self.facing == 6:
                    self.movement[0] -= 2
                    self.movement[1] -= 1
                elif self.facing == 7:
                    self.movement[0] -= 2

                self.walk_frames -= 1
            else:
                self.moving = False

        x = int((int(self.start_pos[0]) + self.position[0] + self.movement[0]) - (self.sprite_size / 2))
        y = int((int(self.start_pos[1]) + self.position[1] + self.movement[1]) - (self.sprite_size / 2))

        self.position = x, y

        sprite_sheet = self.sprite_sheets[self.motion_type]

        sprite_crop = [self.frame_index * self.sprite_size,
                       self.facing * self.sprite_size,
                       self.sprite_size,
                       self.sprite_size]

        sprite = sprite_sheet.subsprite(sprite_crop)
        sprite.position = self.position
        self.sprites.append(sprite)

        """
        renderer = self.renderer.renderer
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

        SDL_RenderCopy(renderer, sprite.texture, src_rect, dest_rect)
        """
    def get_sprites(self):
        return self.sprites