# -*- coding: utf-8 -*-

from sdl2 import SDL_FreeSurface, \
    SDL_CreateRGBSurface, \
    SDL_SWSURFACE, \
    SDL_BlitSurface, \
    SDL_Rect

from sdl2.ext import line, \
    load_image, \
    subsurface, \
    SoftwareSprite

from pytmx import TiledTileLayer, TiledMap

from const import WindowSize, Colors


class Map(SoftwareSprite):
    def __init__(self, map_name, draw_layer="background"):
        self.tiles = Tiles(map_name)
        self.tiles.update_map()
        self.surface = self.tiles.get_sprite(draw_layer)
        self.free = True

        super(Map, self).__init__(self.surface.contents, self.free)


class Tiles:
    def __init__(self, map_name):

        tm = TiledMap(map_name)
        self.size = tm.width * tm.tilewidth, tm.height * tm.tileheight
        self.tmx_data = tm
        self.position = [0, 0]

        self.image_file, _, _ = self.tmx_data.get_tile_image(0, 0, 0)

        self.map_tiles = {}

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

        tw = self.tmx_data.tilewidth
        th = self.tmx_data.tileheight
        pos = self.position
        draw_layer = ""

        background = layer.properties['background']

        tile_position = [0, 0]

        surface = SDL_CreateRGBSurface(SDL_SWSURFACE,
                                       self.size[0],
                                       self.size[1],
                                       32,
                                       0x000000FF,
                                       0x0000FF00,
                                       0x00FF0000,
                                       0xFF000000)

        # iterate over the tiles in the layer
        if background == "true":

            for x, y, data in layer.tiles():
                tile_crop = data[1]

                tile_position[0] = int(((x - y) * tw / 2) + pos[0] + (self.size[0] / 2))
                tile_position[1] = int(((x + y) * th / 2) + pos[1])

                tile = subsurface(self.tile_set, tile_crop)

                rect = SDL_Rect(tile_position[0], tile_position[1])

                SDL_BlitSurface(tile, None, surface, rect)

            self.tiles["background"] = surface
        """
        if background == "false":
            for x, y, data in layer.tiles():
                tile_crop = data[1]

                tile_position[0] = int(((x - y) * tw / 2) + pos[0] + (self.size[0] / 2))
                tile_position[1] = int(((x + y) * th / 2) + pos[1])

                if tile_position[1] < (WindowSize.HEIGHT /2) - 72:
                    tile = subsurface(self.tile_set, tile_crop)
                    rect = SDL_Rect(tile_position[0], tile_position[1])
                    SDL_BlitSurface(tile, None, surface, rect)
                    draw_layer = "behind"
                else:
                    pass
                    tile = subsurface(self.tile_set, tile_crop)
                    rect = SDL_Rect(tile_position[0], tile_position[1])
                    SDL_BlitSurface(tile, None, surface, rect)
                    draw_layer = "front"

            self.tiles[draw_layer] = surface
            """
    def update_map(self):
        for layer in self.tmx_data.visible_layers:
            if isinstance(layer, TiledTileLayer):
                self.update_tile_layer(layer)

                # self.draw_blocking_elements()

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
