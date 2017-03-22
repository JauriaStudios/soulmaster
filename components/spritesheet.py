# -*- coding: utf-8 -*-

from sdl2 import SDL_BlitSurface, \
    SDL_CreateRGBSurface, \
    SDL_SWSURFACE, \
    SDL_Rect

from sdl2.ext import Resources, \
    SoftwareSprite, \
    load_image, \
    subsurface

from components.motion import MotionType

RESOURCES = Resources(__file__, '..', 'resources')


class SpriteSheet:
    """ Sprite sheet """

    def __init__(self, name):
        super(SpriteSheet, self).__init__()

        self.name = name

        self.frame = 0

        self.motion_types = MotionType().get_all()
        self.motion_type = 0

        self.facing = 0

        self.sprite = None
        self.sprite_surface = None

        self.sprite_size = 128, 128

        self.sprites_path = {}

        for k, v in self.motion_types.items():
            self.sprites_path[v] = RESOURCES.get_path("{0}_{1}.png".format(self.name, k))

        self.surfaces = {}
        self.surfaces_size = {}
        self.surfaces_with = []
        self.surfaces_height = 0

        for k, v in self.sprites_path.items():
            self.surfaces[k] = load_image(v)
            self.surfaces_size[k] = self.surfaces[k].w, self.surfaces[k].h
            self.surfaces_with.append(self.surfaces[k].w)
            self.surfaces_height += self.surfaces[k].h
            self.surface_height = self.surfaces[k].h

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
        for filename, surface in self.surfaces.items():
            vertical_offset = i * self.surfaces[filename].h
            rect = SDL_Rect(0, vertical_offset, self.surfaces[filename].w, self.surfaces[filename].h)
            SDL_BlitSurface(surface, None, self.surface, rect)
            i += 1

    def get_surface(self, frame, motion_type, facing):

        self.frame = frame
        self.motion_type = motion_type
        self.facing = facing

        crop = self.frame * self.sprite_size[0], \
            self.facing * self.sprite_size[1] + self.surface_height * self.motion_type, \
            self.sprite_size[0], self.sprite_size[1]

        self.sprite_surface = subsurface(self.surface.contents, crop)

        return self.sprite_surface

    def get_sprite(self):
        surface = self.get_surface(0, 0, 0)
        return SoftwareSprite(surface, True)

    def get_sprite_sheet_width(self, motion_type):
        return self.surfaces[motion_type].w
