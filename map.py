# -*- coding: utf-8 -*-

from sdl2 import SDL_CreateRGBSurface, \
    SDL_SWSURFACE, \
    SDL_BlitSurface, \
    SDL_Rect

from sdl2.ext import Resources, \
    load_image, \
    subsurface, \
    SoftwareSprite

from pytmx import TiledTileLayer, \
    TiledMap, \
    convert_to_bool

from const import WindowSize

MAPS = Resources(__file__, 'resources', 'maps')


class Map(SoftwareSprite):
    def __init__(self, map_name, draw_layer):
        self.free = True
        self.tiles = Tiles(map_name)
        self.tiles.update_map()
        self.surfaces = self.tiles.get_sprite()
        self.surface = self.surfaces[draw_layer]

        super(Map, self).__init__(self.surface.contents, self.free)


class Tiles:
    def __init__(self, map_name):

        self.tile_sets = {}

        tm = TiledMap(map_name)
        self.size = tm.width * tm.tilewidth, tm.height * tm.tileheight
        self.tmx_data = tm
        self.position = [0, 0]

        for tile_set in self.tmx_data.tilesets:
            name = tile_set.name
            tile_set_path = MAPS.get_path("{0}.png".format(name))
            self.tile_sets[tile_set_path] = load_image(tile_set_path)

        """
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
        """

        layers = "background", "behind", "front"
        self.surfaces = {}

        for layer in layers:
            self.surfaces[layer] = SDL_CreateRGBSurface(SDL_SWSURFACE,
                                                        self.size[0],
                                                        self.size[1],
                                                        32,
                                                        0x000000FF,
                                                        0x0000FF00,
                                                        0x00FF0000,
                                                        0xFF000000)

    def update_tile_layer(self, layer):

        tw = self.tmx_data.tilewidth
        th = self.tmx_data.tileheight
        position = self.position

        tile_position = [0, 0]

        if "background" in layer.properties:
            background = convert_to_bool(layer.properties['background'])
            if background:
                for x, y, data in layer.tiles():
                    tile_set = data[0]
                    tile_crop = data[1]

                    tile_position[0] = int(((x - y) * tw / 2) + position[0] + (self.size[0] / 2) - (tw / 2))
                    tile_position[1] = int(((x + y) * th / 2) + position[1])

                    tile = subsurface(self.tile_sets[tile_set], tile_crop)

                    rect = SDL_Rect(tile_position[0], tile_position[1])

                    SDL_BlitSurface(tile, None, self.surfaces["background"], rect)
            elif not background:
                for x, y, data in layer.tiles():
                    tile_set = data[0]
                    tile_crop = data[1]

                    tile_position[0] = int(((x - y) * tw / 2) + position[0] + (self.size[0] / 2))
                    tile_position[1] = int(((x + y) * th / 2) + position[1] - 72)

                    if tile_position[1] < (WindowSize.HEIGHT / 2):
                        tile = subsurface(self.tile_sets[tile_set], tile_crop)
                        rect = SDL_Rect(tile_position[0], tile_position[1])
                        SDL_BlitSurface(tile, None, self.surfaces["behind"], rect)
                    else:
                        pass
                        tile = subsurface(self.tile_sets[tile_set], tile_crop)
                        rect = SDL_Rect(tile_position[0], tile_position[1])
                        SDL_BlitSurface(tile, None, self.surfaces["front"], rect)

    def update_map(self):
        for layer in self.tmx_data.visible_layers:
            if isinstance(layer, TiledTileLayer):
                self.update_tile_layer(layer)

                # self.draw_blocking_elements()

    def get_sprite(self):
        return self.surfaces

    """
    def draw_blocking_elements(self):

        surface = self.lines_surface
        color = Colors.RED
        points = []

        for block in self.blocking_elements:
            for lines in block.points:
                points.append(round(lines[0]) + self.position[0])
                points.append(round(lines[1]) + self.position[1])

        line(surface, color, points)
    """
