#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys

# If we're on Windows, use the included compiled DLLs.
if sys.platform == "win32":
    os.environ["PYSDL2_DLL_PATH"] = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'libs')

from sdl2 import *
import sdl2.ext

from const import WindowSize
from menu import Menu


def main():
    screen_size = (WindowSize.WIDTH, WindowSize.HEIGHT)

    sdl2.ext.init()

    window = sdl2.ext.Window("Soul Master", size=screen_size)
    window.renderer = sdl2.ext.Renderer(window, SDL_RENDERER_ACCELERATED)
    window.renderer.color = 0, 0, 0, 0
    window.show()

    menu = Menu(window, window.renderer)
    menu.run()

if __name__ == '__main__':
    main()
