# -*- coding: utf-8 -*-

import os
import sys

# If we're on Windows, use the included compiled DLLs.
if sys.platform == "win32":
    os.environ["PYSDL2_DLL_PATH"] = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'libs')

import sdl2
import sdl2.ext

from pytmx import *
from pytmx.util_pysdl2 import load_pysdl2

from const import WindowSize


class TiledRenderer(object):
    def __init__(self, filename, renderer):
        tm = load_pysdl2(renderer, filename)
        self.size = tm.width * tm.tilewidth, tm.height * tm.tileheight
        self.tmx_data = tm
        self.renderer = renderer
        self.pos = (0, 0)

        logger.info("Objects in map:")
        for obj in self.tmx_data.objects:
            logger.info(obj)
            for k, v in obj.properties.items():
                logger.info("{0}\t{1}".format(k, v))

        logger.info("GID (tile) properties:")
        for k, v in self.tmx_data.tile_properties.items():
            logger.info("{0}\t{1}".format(k, v))

    def render_tile_layer(self, layer):
        # deref these heavily used references for speed
        window_x = WindowSize.WIDTH
        window_y = WindowSize.HEIGHT
        tw = self.tmx_data.tilewidth
        th = self.tmx_data.tileheight
        renderer = self.renderer.renderer
        dest = sdl2.rect.SDL_Rect(0, 0, tw, th + 96)
        rce = sdl2.SDL_RenderCopyEx

        # iterate over the tiles in the layer
        for x, y, tile in layer.tiles():
            texture, src, flip = tile
            dest.x = int(((x - y) * tw / 2) + window_x / 2) + self.pos[0]
            dest.y = int(((x + y) * th / 2) - window_y / 8) + self.pos[1]
            angle = 90 if (flip & 4) else 0
            rce(renderer, texture, src, dest, angle, None, flip)

    def render_map(self):
        for layer in self.tmx_data.visible_layers:
            # draw map tile layers
            if isinstance(layer, TiledTileLayer):
                self.render_tile_layer(layer)

    def update(self, position):
        self.pos = position

