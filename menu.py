# -*- coding: utf-8 -*-

import os
import sys

# If we're on Windows, use the included compiled DLLs.
if sys.platform == "win32":
    os.environ["PYSDL2_DLL_PATH"] = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'libs')

from sdl2 import *
import sdl2.ext
import sdl2.sdlttf

from const import WindowSize

RESOURCES = sdl2.ext.Resources(__file__, 'resources')


class Menu:
    def __init__(self, renderer):
        self.renderer = renderer

        self.menu_bg = RESOURCES.get_path("menu_bg.png")
        self.menu_cursor = RESOURCES.get_path("menu_cursor.png")

        self.factory = sdl2.ext.SpriteFactory(
            sdl2.ext.TEXTURE,
            renderer=self.renderer
        )

        self.cursor_position = [0, 0]
        self.cursor_sprite_size = 64

        self.menu_bg_sprite = self.init_sprite(self.menu_bg)
        self.menu_cursor_sprite = self.init_sprite(self.menu_cursor)

    def init_sprite(self, file_path):
        sprite_surface = self.factory.from_image(file_path)
        return sprite_surface

    def update(self, elapsed_time):
        pass

    def draw(self):

        renderer = self.renderer.renderer

        sprite_size = self.cursor_sprite_size

        menu_bg = self.menu_bg_sprite
        menu_cursor = self.menu_cursor_sprite

        bg_src_rect = SDL_Rect()

        bg_src_rect.x = 0
        bg_src_rect.y = 0
        bg_src_rect.w = sprite_size
        bg_src_rect.h = sprite_size

        bg_dest_rect = SDL_Rect()

        bg_dest_rect.x = 0
        bg_dest_rect.y = 0
        bg_dest_rect.w = WindowSize.WIDTH
        bg_dest_rect.h = WindowSize.HEIGHT

        cursor_src_rect = SDL_Rect()

        cursor_src_rect.x = 0
        cursor_src_rect.y = 0
        cursor_src_rect.w = sprite_size
        cursor_src_rect.h = sprite_size

        cursor_dest_rect = SDL_Rect()

        cursor_dest_rect.x = int((WindowSize.WIDTH / 2) - (sprite_size / 2))
        cursor_dest_rect.y = int((WindowSize.HEIGHT / 2) - (sprite_size / 2))
        cursor_dest_rect.w = sprite_size
        cursor_dest_rect.h = sprite_size

        render.SDL_RenderCopy(renderer, menu_bg.texture, bg_src_rect, bg_dest_rect)
        render.SDL_RenderCopy(renderer, menu_cursor.texture, cursor_src_rect, cursor_dest_rect)
