# -*- coding: utf-8 -*-

from sdl2 import SDL_RenderCopyEx, SDL_Rect
from sdl2.ext import line

from pytmx import *
from pytmx.util_pysdl2 import load_pysdl2

from const import WindowSize, Colors


class TiledRenderer:
    def __init__(self, filename, window, renderer):

        self.window = window
        self.renderer = renderer

        tm = load_pysdl2(self.renderer, filename)
        self.size = tm.width * tm.tilewidth, tm.height * tm.tileheight
        self.tmx_data = tm
        self.pos = (0, 0)

        self.blocking_elements = []

        print("Objects in map:")
        for obj in self.tmx_data.objects:
            print(obj)
            print("BLOCK\t{0}".format(obj.points))
            for k, v in obj.properties.items():
                print("PROPS\t{0}\t{1}".format(k, v))
                if (k == "block") and (v == "true"):
                    print("FOUND BLOCK")
                    self.blocking_elements.append(obj)

        print("GID (tile) properties:")
        for k, v in self.tmx_data.tile_properties.items():
            logger.info("{0}\t{1}".format(k, v))

    def render_tile_layer(self, layer, level):
        # deref these heavily used references for speed
        window_x = WindowSize.WIDTH
        window_y = WindowSize.HEIGHT

        renderer = self.renderer.renderer

        tw = self.tmx_data.tilewidth
        th = self.tmx_data.tileheight
        pos = self.pos

        dest = SDL_Rect(0, 0, tw, th + 96)
        rce = SDL_RenderCopyEx

        background = layer.properties['background']

        # iterate over the tiles in the layer
        if (background == "true") and (level == "back"):
            for x, y, tile in layer.tiles():
                texture, src, flip = tile

                dest.x = int(((x - y) * tw / 2) + window_x / 2) + pos[0]
                dest.y = int(((x + y) * th / 2) - window_y / 8) + pos[1]

                angle = 90 if (flip & 4) else 0

                rce(renderer, texture, src, dest, angle, None, flip)

        elif (background == "false") and (level == "up"):
            for x, y, tile in layer.tiles():

                texture, src, flip = tile

                dest.x = int(((x - y) * tw / 2) + window_x / 2) + pos[0]
                dest.y = int(((x + y) * th / 2) - window_y / 8) + pos[1]

                angle = 90 if (flip & 4) else 0

                if dest.y < (window_y / 2) - 72:
                    rce(renderer, texture, src, dest, angle, None, flip)

        elif (background == "false") and (level == "down"):
            for x, y, tile in layer.tiles():

                texture, src, flip = tile

                dest.x = int(((x - y) * tw / 2) + window_x / 2) + pos[0]
                dest.y = int(((x + y) * th / 2) - window_y / 8) + pos[1]

                angle = 90 if (flip & 4) else 0

                if dest.y >= (window_y / 2) - 72:
                    rce(renderer, texture, src, dest, angle, None, flip)

    def render_map(self, level):
        for layer in self.tmx_data.visible_layers:
            if isinstance(layer, TiledTileLayer):
                self.render_tile_layer(layer, level)

        # self.draw_blocking_elements()

    def update(self, position, elapsed_time):
        self.pos = position

    def draw_blocking_elements(self):

        surf = self.window.get_surface()
        color = Colors.RED
        points = []

        for block in self.blocking_elements:
            for lines in block.points:
                points.append(round(lines[0]) + self.pos[0])
                points.append(round(lines[1]) + self.pos[1])

        line(surf, color, points)
