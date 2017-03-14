# -*- coding: utf-8 -*-

from sdl2 import SDL_Quit,\
    SDL_GetTicks,\
    SDL_KEYUP,\
    SDL_KEYDOWN,\
    SDL_QUIT,\
    SDL_Delay
from sdl2 import SDLK_ESCAPE,\
    SDLK_RIGHT,\
    SDLK_UP,\
    SDLK_DOWN,\
    SDLK_LEFT,\
    SDLK_SPACE,\
    SDLK_i
from sdl2.ext import Resources,\
    get_events

from const import WindowSize
from input import Input
from db import DataBase
from map import TiledRenderer
from player import Player, Facing, MotionType
from npc import NPC
from enemy import Enemy

FPS = 30  # units.FPS
MAX_FRAME_TIME = int(5 * (1000 / FPS))

RESOURCES = Resources(__file__, 'resources')
MAPS = Resources(__file__, 'resources', 'maps')


class Game(object):
    def __init__(self, window, world, renderer, factory):

        self.db = DataBase()

        map_file = MAPS.get_path("map.tmx")

        self.running = False
        self.window = window
        self.window_size = window.size
        self.world = world
        self.renderer = renderer
        self.factory = factory

        # self.map_renderer = TiledRenderer(map_file, self.window, self.renderer)

        self.sprites = []

        self.player = Player(self.window, self.renderer, self.factory)
        self.player_sprites = None

        self.all_npc = []
        self.init_npc("Debug Room")

        self.doombat = Enemy(self.renderer, self.factory, "doombat")

        self.entities = [
            self.player,
            self.doombat
        ]

        self.player_layer = 0
        self.enemy_layer = 0

    def __del__(self):
        SDL_Quit()

    def init_npc(self, map):

        map_data = self.db.get_map_npc(map)

        map_npc = []

        for data in map_data:
            map_npc.append(data["npc"])

        for npc in map_npc:
            self.all_npc.append(NPC(self.window, self.renderer, self.factory, npc))

    def update(self, position, elapsed_time):
        # for npc in self.all_npc:
        #    npc.update(position, elapsed_time)
        pass

    def map_update(self, pos, elapsed_time):
        # self.map_renderer.update(pos, elapsed_time)
        pass

    def player_update(self, motion_type, facing, elapsed_time):
        self.player.update(motion_type, facing, elapsed_time)

    def enemy_update(self, pos, elapsed_time):
        self.doombat.update(pos, elapsed_time)

    def get_sprites(self):

        # self.map_renderer.render_map("back")
        # self.map_renderer.render_map("up")

        self.player_sprites = self.player.get_sprite()

        for sprite in self.player_sprites:
            self.sprites.append(sprite)

        self.player_sprites.clear()

        """
        for npc in self.all_npc:
            npc.draw()

        self.doombat.draw()
        """
        # self.map_renderer.render_map("down")

    def run(self):

        window = self.window

        game_input = Input()

        speed_x, speed_y = 2, 1
        player_pos = [0, 0]

        motion_type = self.player.motion_type
        facing = self.player.facing

        running = True
        last_update_time = SDL_GetTicks()  # units.MS

        while running:
            start_time = SDL_GetTicks()  # units.MS

            game_input.begin_new_frame()
            game_events = get_events()

            for event in game_events:
                if event.type == SDL_KEYDOWN:
                    game_input.key_down_event(event)

                elif event.type == SDL_KEYUP:
                    game_input.key_up_event(event)

                elif event.type == SDL_QUIT:
                    running = False
                    break

            # Exit
            if game_input.was_key_pressed(SDLK_ESCAPE):
                running = False

            # Player movement
            if game_input.is_key_held(SDLK_RIGHT) and game_input.is_key_held(SDLK_UP):
                player_pos[0] -= speed_x
                player_pos[1] += speed_y
                motion_type = MotionType.WALKING
                facing = Facing.RIGHT_UP
            elif game_input.is_key_held(SDLK_RIGHT) and game_input.is_key_held(SDLK_DOWN):
                player_pos[0] -= speed_x
                player_pos[1] -= speed_y
                motion_type = MotionType.WALKING
                facing = Facing.RIGHT_DOWN
            elif game_input.is_key_held(SDLK_LEFT) and game_input.is_key_held(SDLK_UP):
                player_pos[0] += speed_x
                player_pos[1] += speed_y
                motion_type = MotionType.WALKING
                facing = Facing.LEFT_UP
            elif game_input.is_key_held(SDLK_LEFT) and game_input.is_key_held(SDLK_DOWN):
                player_pos[0] += speed_x
                player_pos[1] -= speed_y
                motion_type = MotionType.WALKING
                facing = Facing.LEFT_DOWN
            elif game_input.is_key_held(SDLK_LEFT):
                player_pos[0] += speed_x
                motion_type = MotionType.WALKING
                facing = Facing.LEFT
            elif game_input.is_key_held(SDLK_RIGHT):
                player_pos[0] -= speed_x
                motion_type = MotionType.WALKING
                facing = Facing.RIGHT
            elif game_input.is_key_held(SDLK_UP):
                player_pos[1] += speed_y
                motion_type = MotionType.WALKING
                facing = Facing.UP
            elif game_input.is_key_held(SDLK_DOWN):
                player_pos[1] -= speed_y
                motion_type = MotionType.WALKING
                facing = Facing.DOWN

            elif game_input.was_key_pressed(SDLK_i):
                self.player.toggle_inventory()

            # Player Attack
            elif game_input.is_key_held(SDLK_SPACE):
                motion_type = MotionType.CASTING

            # Nothing
            else:
                motion_type = MotionType.STANDING

            current_time = SDL_GetTicks()  # units.MS
            elapsed_time = current_time - last_update_time  # units.MS

            self.update(player_pos, min(elapsed_time, MAX_FRAME_TIME))

            # self.map_update(player_pos, min(elapsed_time, MAX_FRAME_TIME))
            self.player_update(motion_type, facing, min(elapsed_time, MAX_FRAME_TIME))
            self.enemy_update(player_pos, min(elapsed_time, MAX_FRAME_TIME))

            last_update_time = current_time

            self.get_sprites()

            self.renderer.render(self.sprites)
            self.sprites.clear()
            # window.refresh()

            # This loop lasts 1/60th of a second, or 1000/60th ms
            ms_per_frame = 1000 // FPS  # units.MS
            elapsed_time = SDL_GetTicks() - start_time  # units.MS
            if elapsed_time < ms_per_frame:
                SDL_Delay(ms_per_frame - elapsed_time)
