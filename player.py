# -*- coding: utf-8 -*-

from sdl2 import SDL_BlitSurface, \
    SDL_CreateRGBSurface, \
    SDL_SWSURFACE, \
    SDL_Rect

from sdl2.ext import Resources, \
    Entity, \
    SoftwareSprite, \
    load_image

from const import WindowSize
from components.frames import Frames
from components.motion import MotionType
from components.facing import Facing
from spell import Spell
from inventory import Inventory

RESOURCES = Resources(__file__, 'resources')


class Player(Entity):
    def __init__(self, world):
        self.frames = Frames()
        self.motion_types = MotionType()
        self.facing = Facing()

        player_sprite_sheet = PlayerSpriteSheet()
        self.sprite = SoftwareSprite(player_sprite_sheet.get_surface(), True)

        self.player_data = PlayerData()


class PlayerData:
    def __init__(self):
        super(PlayerData, self).__init__()
        self.life = 100


class PlayerSpriteSheet:
    """ Player sprite sheet """
    def __init__(self):
        super(PlayerSpriteSheet, self).__init__()

        self.motion_type = MotionType()
        self.motion_types = self.motion_type.get_all()
        self.sprite_size = 128, 128

        self.sprites_path = {}

        for k, v in self.motion_types.items():
            self.sprites_path[v] = RESOURCES.get_path("{0}_{1}.png".format("player", k))

        self.surfaces = {}
        self.surfaces_size = {}
        self.surfaces_with = []
        self.surfaces_height = 0

        for k, v in self.sprites_path.items():
            self.surfaces[k] = load_image(v)
            self.surfaces_size[k] = self.surfaces[k].w, self.surfaces[k].h
            self.surfaces_with.append(self.surfaces[k].w)
            self.surfaces_height += self.surfaces[k].h

        self.surfaces_with = max(self.surfaces_with)

        self.surface = SDL_CreateRGBSurface(SDL_SWSURFACE,
                                            self.surfaces_with,
                                            self.surfaces_height,
                                            32,
                                            0x000000FF,
                                            0x0000FF00,
                                            0x00FF0000,
                                            0xFF000000)
        i = 0
        for name, surface in self.surfaces.items():
            vertical_offset = i * self.surfaces[name].h
            rect = SDL_Rect(0, vertical_offset, self.surfaces[name].w, self.surfaces[name].h)
            SDL_BlitSurface(surface, None, self.surface, rect)
            i += 1

    def get_surface(self):
        return self.surface.contents
