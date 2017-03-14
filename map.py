# -*- coding: utf-8 -*-

from sdl2 import SDL_FreeSurface

from sdl2.ext import line,\
    load_image, \
    subsurface, \
    SoftwareSprite

from pytmx import TiledTileLayer, TiledMap

from const import WindowSize, Colors


class Map(SoftwareSprite):
    def __init__(self, map_name):
        self.tiles = Tiles(map_name)
        self.tiles.update_map()
        self.surfaces = self.tiles.get_sprite("background")
        self.free = True

        for surf in self.surfaces:
            self.surface = surf

        super(Map, self).__init__(self.surface, self.free)


class Tiles:
    def __init__(self, map_name):

        tm = TiledMap(map_name)
        self.size = tm.width * tm.tilewidth, tm.height * tm.tileheight
        self.tmx_data = tm
        self.position = [0, 0]

        self.image_file, _, _ = self.tmx_data.get_tile_image(0, 0, 0)

        self.tile_set = load_image(self.image_file)
        self.tiles = {}

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
            print("{0}\t{1}".format(k, v))

    def update_tile_layer(self, layer):
        window_x = WindowSize.WIDTH
        window_y = WindowSize.HEIGHT

        tw = self.tmx_data.tilewidth
        th = self.tmx_data.tileheight
        pos = self.position

        tiles = []

        background = layer.properties['background']

        tile_position = [0, 0]

        # iterate over the tiles in the layer
        if background == "true":
            for x, y, data in layer.tiles():

                tile_crop = data[1]

                tile_position[0] = int(((x - y) * tw / 2) + window_x / 2) + pos[0]
                tile_position[1] = int(((x + y) * th / 2) - window_y / 8) + pos[1]

                tile = subsurface(self.tile_set, tile_crop)
                tile.position = tile_position

                tiles.append(tile)

                self.tiles["background"] = tiles

        """
        elif (background == "false") and (draw_layer == "up"):
            for x, y, tile in layer.tiles():

                texture, src, flip = tile

                dest.x = int(((x - y) * tw / 2) + window_x / 2) + pos[0]
                dest.y = int(((x + y) * th / 2) - window_y / 8) + pos[1]

                angle = 90 if (flip & 4) else 0

                if dest.y < (window_y / 2) - 72:
                    SDL_RenderCopy(renderer, texture, src, dest, angle, None, flip)

        elif (background == "false") and (draw_layer == "down"):
            for x, y, tile in layer.tiles():

                texture, src, flip = tile

                dest.x = int(((x - y) * tw / 2) + window_x / 2) + pos[0]
                dest.y = int(((x + y) * th / 2) - window_y / 8) + pos[1]

                angle = 90 if (flip & 4) else 0

                if dest.y >= (window_y / 2) - 72:
                    rce(renderer, texture, src, dest, angle, None, flip)
        """

    def update_map(self):
        for layer in self.tmx_data.visible_layers:
            if isinstance(layer, TiledTileLayer):
                self.update_tile_layer(layer)

                # self.draw_blocking_elements()

    def update(self, position, elapsed_time):
        self.position = position
        self.update_map()

    def get_sprite(self, draw_layer):
        return self.tiles[draw_layer]

    """
    def draw_blocking_elements(self):

        surf = self.window.get_surface()
        color = Colors.RED
        points = []

        for block in self.blocking_elements:
            for lines in block.points:
                points.append(round(lines[0]) + self.pos[0])
                points.append(round(lines[1]) + self.pos[1])

        line(surf, color, points)
    """
