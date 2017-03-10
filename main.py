#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from sdl2 import SDL_RENDERER_ACCELERATED
from sdl2.ext import Window, Renderer, init

from const import WindowSize
from menu import Menu


def main():
    screen_size = (WindowSize.WIDTH, WindowSize.HEIGHT)

    init()

    window = Window("Soul Master", size=screen_size)
    window.renderer = Renderer(window)  # , SDL_RENDERER_ACCELERATED)
    window.renderer.color = 0, 0, 0, 0
    window.show()

    menu = Menu(window, window.renderer)
    menu.run()

if __name__ == '__main__':
    main()
