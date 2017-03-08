# -*- coding: utf-8 -*-

import os
import sys
import logging

# If we're on Windows, use the included compiled DLLs.
if sys.platform == "win32":
    os.environ["PYSDL2_DLL_PATH"] = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'libs')

from sdl2 import *
import sdl2.ext

from const import WindowSize
from input import Input
from db import DataBase
from map import TiledRenderer
from player import Player, Facing, MotionType
from npc import NPC
from enemy import Enemy

logger = logging.getLogger(__name__)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
logger.addHandler(ch)
logger.setLevel(logging.INFO)

FPS = 60  # units.FPS
MAX_FRAME_TIME = int(5 * (1000 / FPS))

RESOURCES = sdl2.ext.Resources(__file__, 'resources')
MAPS = sdl2.ext.Resources(__file__, 'resources', 'maps')


class Game(object):
    def __init__(self, window, renderer):

        self.db = DataBase()

        map_file = MAPS.get_path("map.tmx")

        self.running = False
        self.window = window
        self.window_size = window.size
        self.sdl_renderer = renderer

        self.map_renderer = TiledRenderer(map_file, self.window, self.sdl_renderer)

        self.player = Player(self.sdl_renderer)

        self.all_npc = []
        self.init_npc("debug_room")

        self.doombat = Enemy(self.sdl_renderer, "doombat")

        self.entities = [
            self.player,
            self.doombat
        ]

        self.player_layer = 0
        self.enemy_layer = 0

    def __del__(self):
        SDL_Quit()

    def init_npc(self, map):

        all_npc_names = self.db.get_all_npc()

        for data in all_npc_names:
            npc = NPC(self.window, self.sdl_renderer, data)
            self.all_npc.append(npc)

    def update(self, position, elapsed_time):
        for npc in self.all_npc:
            npc.update(position, elapsed_time)

    def map_update(self, pos, elapsed_time):
        self.map_renderer.update(pos, elapsed_time)

    def player_update(self, motion_type, facing, elapsed_time):
        self.player.update(motion_type, facing, elapsed_time)

    def enemy_update(self, pos, elapsed_time):
        self.doombat.update(pos, elapsed_time)

    def draw(self):
        self.sdl_renderer.clear()

        self.map_renderer.render_map("back")
        self.map_renderer.render_map("up")

        self.player.draw()

        for npc in self.all_npc:
            npc.draw()

        self.doombat.draw()

        self.map_renderer.render_map("down")

        self.sdl_renderer.present()

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
            game_events = sdl2.ext.get_events()

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

            # Player Attack
            elif game_input.is_key_held(SDLK_SPACE):
                motion_type = MotionType.PRECAST

            # Nothing
            else:
                motion_type = MotionType.STANDING

            current_time = SDL_GetTicks()  # units.MS
            elapsed_time = current_time - last_update_time  # units.MS

            self.update(player_pos, min(elapsed_time, MAX_FRAME_TIME));

            self.map_update(player_pos, min(elapsed_time, MAX_FRAME_TIME))
            self.player_update(motion_type, facing, min(elapsed_time, MAX_FRAME_TIME))
            self.enemy_update(player_pos, min(elapsed_time, MAX_FRAME_TIME))

            last_update_time = current_time

            self.draw()
            window.refresh()

            # This loop lasts 1/60th of a second, or 1000/60th ms
            ms_per_frame = 1000 // FPS  # units.MS
            elapsed_time = SDL_GetTicks() - start_time  # units.MS
            if elapsed_time < ms_per_frame:
                SDL_Delay(ms_per_frame - elapsed_time)
