#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys

# If we're on Windows, use the included compiled DLLs.
if sys.platform == "win32":
    os.environ["PYSDL2_DLL_PATH"] = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'libs')

from sdl2 import *
from sdl2.sdlttf import *
import sdl2.ext


FONTS = sdl2.ext.Resources(__file__, 'resources', 'fonts')


class Dialog(object):
    def __init__(self, window, text_color, text_size, text_position, dialog_color, dialog_size):
        TTF_Init()

        self.window = window
        self.window_size = window.size
        self.sdl_renderer = window.renderer

        self.text_color = text_color
        self.text_size = text_size
        self.text_position = text_position
        self.dialog_color = dialog_color
        self.dialog_size = dialog_size

        self.font_path = FONTS.get_path("04B_20__.TTF")

        self.image = None

    def __del__(self):
        TTF_Quit()

    def render_text(self, message, font_file, font_color, font_size):
        SDL_ClearError()
        font = TTF_OpenFont(font_file.encode("UTF-8"), font_size)

        if font is None:
            return None

        surf = TTF_RenderText_Blended(font, message.encode("UTF-8"), font_color)

        if surf is None:
            TTF_CloseFont(font)
            return None

        texture = SDL_CreateTextureFromSurface(self.sdl_renderer.renderer, surf)
        if texture is None:
            return None

        SDL_FreeSurface(surf)
        TTF_CloseFont(font)
        return texture

    def draw(self, messages):
        for index, text in messages.items():
            self.image = self.render_text(
                            text,
                            self.font_path,
                            self.text_color,
                            self.text_size
                        )

            dest = SDL_Rect(self.text_position[0], (self.text_position[1] +(64 * index)))
            dest.w = 300
            dest.h = 32

            SDL_RenderCopy(self.sdl_renderer.renderer, self.image, None, dest)
