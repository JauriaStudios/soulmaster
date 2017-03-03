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
    def __init__(self, window, text_color, text_size, dialog_color, dialog_size):
        TTF_Init()

        self.window = window
        self.window_size = window.size
        self.sdl_renderer = window.renderer

        self.text_color = text_color
        self.text_size = text_size
        self.dialog_color = dialog_color
        self.dialog_size = dialog_size

        self.font_path = FONTS.get_path("Glametrix.otf")

        self.image = []

    def __del__(self):
        TTF_Quit()

    def render_texture(self, texture, renderer, position, size):

        dest = SDL_Rect()
        dest.x = position[0]
        dest.y = position[1]
        dest.w = size[0]
        dest.h = size[1]

        SDL_RenderCopy(renderer, texture, None, dest)

    def render_text(self, line, message, font_file, font_color, font_size, renderer):
        SDL_ClearError()
        font = TTF_OpenFont(font_file, font_size)
        p = SDL_GetError()
        if font is None or not p == '':
            print("TTF_OpenFont error: " + p)
            return None

        #We need to first render to a surface as that's what TTF_RenderText
        #returns, then load that surface into a texture
        surf = TTF_RenderText_Blended(font, message, font_color)

        if surf is None:
            TTF_CloseFont(font)
            print("TTF_RenderText")
            return None

        texture = SDL_CreateTextureFromSurface(renderer, surf)
        if texture is None:
            print("CreateTexture")

        #Clean up the surface and font

        SDL_FreeSurface(surf)
        TTF_CloseFont(font)
        return texture

    def draw(self, messages):
        for k, text in messages.items():
            self.image.append(self.render_text(k, text, self.font_path, self.text_color, self.text_size, self.sdl_renderer))
