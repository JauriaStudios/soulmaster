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

from const import Colors, WindowSize


RESOURCES = sdl2.ext.Resources(__file__, 'resources')
FONTS = sdl2.ext.Resources(__file__, 'resources', 'fonts')


class Dialog(object):
    def __init__(self, window, text_color, text_size, text_position, dialog_color):
        TTF_Init()

        self.window = window
        self.window_size = window.size
        self.sdl_renderer = window.renderer

        self.text_color = text_color
        self.text_size = text_size
        self.text_position = text_position
        self.dialog_color = dialog_color

        self.font_path = FONTS.get_path("04B_20__.TTF")

        self.image = None

        self.factory = sdl2.ext.SpriteFactory(
            sdl2.ext.TEXTURE,
            renderer=self.sdl_renderer
        )

        border_image_path = RESOURCES.get_path("dialog_border.png")
        self.border = self.factory.from_image(border_image_path)
        self.bg = None

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

        chars = []
        for index, text in messages.items():
            i = 0
            for char in text:
                i += 1
            chars.append(i)

        width = (self.text_size * max(chars))
        height = self.text_size
        x = self.text_position[0]
        y = self.text_position[1]

        renderer = self.sdl_renderer.renderer

        self.bg = self.factory.from_color(Colors.BLACK, size=(width, height))

        bg_dest = SDL_Rect(x - 16,
                           y - 16,
                           width + 32,
                           height * len(messages.items()) + 32)

        SDL_RenderCopy(renderer, self.bg.texture, None, bg_dest)

        border_src = SDL_Rect(0, 0, 16, 16)

        border_dest = SDL_Rect(0, 0, 16, 16)

        cols = int(width / 16) + 3
        rows = int(height / 16) * len(messages.items()) + 3

        for i in range(cols + 1):
            for j in range(rows + 1):
                if (i == 0) and (j == 0):
                    border_src.x = 0
                    border_src.y = 0
                elif (i < cols) and (j == 0):
                    border_src.x = 16
                    border_src.y = 0
                elif (i == cols) and (j == 0):
                    border_src.x = 32
                    border_src.y = 0
                elif (i == cols) and (j < rows):
                    border_src.x = 32
                    border_src.y = 16
                elif (i == 0) and (j < rows):
                    border_src.x = 0
                    border_src.y = 16
                elif (i == 0) and (j == rows):
                    border_src.x = 0
                    border_src.y = 32
                elif (i < cols) and (j == rows):
                    border_src.x = 16
                    border_src.y = 32
                elif (i == cols) and (j == rows):
                    border_src.x = 32
                    border_src.y = 32
                else:
                    border_src.x = 16
                    border_src.y = 16

                border_dest.x = (16 * i) + (x - 32)
                border_dest.y = (16 * j) + (y - 32)

                SDL_RenderCopy(renderer, self.border.texture, border_src, border_dest)

        for index, text in messages.items():
            self.image = self.render_text(
                            text,
                            self.font_path,
                            self.text_color,
                            self.text_size
                        )

            text_dest = SDL_Rect(x, (y + (self.text_size * index)))
            text_dest.w = self.text_size * chars[index]
            text_dest.h = height

            SDL_RenderCopy(renderer, self.image, None, text_dest)
