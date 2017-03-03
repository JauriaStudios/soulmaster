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
from input import Input
from game import Game

FPS = 60  # units.FPS
MAX_FRAME_TIME = int(5 * (1000 / FPS))
RESOURCES = sdl2.ext.Resources(__file__, 'resources')


class Menu:
    def __init__(self, window):
        self.window = window
        self.renderer = window.renderer

        self.menu_bg = RESOURCES.get_path("menu_bg.png")
        self.menu_cursor = RESOURCES.get_path("menu_cursor.png")

        self.factory = sdl2.ext.SpriteFactory(
            sdl2.ext.TEXTURE,
            renderer=self.renderer
        )

        self.cursor_position = [0, 0]
        self.cursor_sprite_size = 64

        self.menu_bg_sprite = self.factory.from_image(self.menu_bg)
        self.menu_cursor_sprite = self.factory.from_image(self.menu_cursor)

    def update(self, elapsed_time):
        pass

    def run(self):

        menu_input = Input()

        running = True
        last_update_time = SDL_GetTicks()  # units.MS

        while running:
            start_time = SDL_GetTicks()  # units.MS

            menu_input.begin_new_frame()
            menu_events = sdl2.ext.get_events()

            for event in menu_events:
                if event.type == SDL_KEYDOWN:
                    menu_input.key_down_event(event)

                elif event.type == SDL_KEYUP:
                    menu_input.key_up_event(event)

                elif event.type == SDL_QUIT:
                    running = False
                    break

            # Exit
            if menu_input.was_key_pressed(SDLK_ESCAPE):
                running = False

            current_time = SDL_GetTicks()  # units.MS
            elapsed_time = current_time - last_update_time  # units.MS

            self.update(min(elapsed_time, MAX_FRAME_TIME));

            last_update_time = current_time

            self.draw()
            self.window.refresh()

            # This loop lasts 1/60th of a second, or 1000/60th ms
            ms_per_frame = 1000 // FPS  # units.MS
            elapsed_time = SDL_GetTicks() - start_time  # units.MS
            if elapsed_time < ms_per_frame:
                SDL_Delay(ms_per_frame - elapsed_time)

    def draw(self):

        renderer = self.renderer.renderer

        cursor_size = self.cursor_sprite_size

        menu_bg = self.menu_bg_sprite
        menu_cursor = self.menu_cursor_sprite

        bg_src_rect = SDL_Rect()

        bg_src_rect.x = 0
        bg_src_rect.y = 0
        bg_src_rect.w = menu_bg.size[0]
        bg_src_rect.h = menu_bg.size[1]

        bg_dest_rect = SDL_Rect()

        bg_dest_rect.x = 0
        bg_dest_rect.y = 0
        bg_dest_rect.w = WindowSize.WIDTH
        bg_dest_rect.h = WindowSize.HEIGHT

        """
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
        """

        render.SDL_RenderCopy(renderer, menu_bg.texture, bg_src_rect, bg_dest_rect)
        # render.SDL_RenderCopy(renderer, menu_cursor.texture, cursor_src_rect, cursor_dest_rect)
