# -*- coding: utf-8 -*-

from sdl2 import SDL_Delay, SDL_GetTicks, SDL_KEYDOWN, SDL_KEYUP, SDL_QUIT, SDL_Rect, SDL_RenderCopy
from sdl2 import SDLK_ESCAPE, SDLK_UP, SDLK_DOWN, SDLK_RETURN
from sdl2.ext import Resources, SpriteFactory, TEXTURE, get_events

from const import WindowSize, Colors
from input import Input
from ui import Dialog
from game import Game

FPS = 60  # units.FPS
MAX_FRAME_TIME = int(5 * (1000 / FPS))
RESOURCES = Resources(__file__, 'resources')


class Menu:
    def __init__(self, window, renderer):
        self.window = window
        self.renderer = renderer
        self.sdl_renderer = renderer.renderer

        self.menu_bg = RESOURCES.get_path("menu_bg.png")
        self.menu_cursor = RESOURCES.get_path("menu_cursor.png")

        self.factory = SpriteFactory(
            TEXTURE,
            renderer=self.renderer
        )

        self.running = True

        self.cursor_position = [0, 0]
        self.cursor_sprite_size = 64

        self.menu_bg_sprite = self.factory.from_image(self.menu_bg)
        self.menu_cursor_sprite = self.factory.from_image(self.menu_cursor)

        self.menu_text = {0: "DEBUG ROOM", 1: "OPTIONS", 2: "EXIT"}
        self.menu_dialog = Dialog(self.window, self.renderer, Colors.WHITE, 32, (300, 200), Colors.BLACK)

    def update(self, elapsed_time):
        pass

    def run(self):

        menu_input = Input()

        last_update_time = SDL_GetTicks()  # units.MS

        while self.running:
            start_time = SDL_GetTicks()  # units.MS

            menu_input.begin_new_frame()
            menu_events = get_events()

            for event in menu_events:
                if event.type == SDL_KEYDOWN:
                    menu_input.key_down_event(event)

                elif event.type == SDL_KEYUP:
                    menu_input.key_up_event(event)

                elif event.type == SDL_QUIT:
                    self.running = False
                    break

            # Exit
            if menu_input.was_key_pressed(SDLK_ESCAPE):
                self.running = False

            # Move the cursor
            elif menu_input.was_key_pressed(SDLK_UP):
                if self.cursor_position[1] != 0:
                    self.cursor_position[1] -= 1
            elif menu_input.was_key_pressed(SDLK_DOWN):
                if self.cursor_position[1] != 2:
                    self.cursor_position[1] += 1

            # Select option
            elif menu_input.was_key_pressed(SDLK_RETURN):
                self.running = False
                if self.cursor_position[1] == 0:
                    self.launch_debug()

            current_time = SDL_GetTicks()  # units.MS
            elapsed_time = current_time - last_update_time  # units.MS

            self.update(min(elapsed_time, MAX_FRAME_TIME))

            last_update_time = current_time

            self.draw()
            self.window.refresh()

            # This loop lasts 1/60th of a second, or 1000/60th ms
            ms_per_frame = 1000 // FPS  # units.MS
            elapsed_time = SDL_GetTicks() - start_time  # units.MS
            if elapsed_time < ms_per_frame:
                SDL_Delay(ms_per_frame - elapsed_time)

    def draw(self):

        renderer = self.sdl_renderer

        menu_text = self.menu_text

        cursor_position = self.cursor_position
        cursor_size = self.cursor_sprite_size

        menu_bg = self.menu_bg_sprite
        menu_cursor = self.menu_cursor_sprite

        bg_dest_rect = SDL_Rect()

        bg_dest_rect.x = 0
        bg_dest_rect.y = 0
        bg_dest_rect.w = WindowSize.WIDTH
        bg_dest_rect.h = WindowSize.HEIGHT

        cursor_dest_rect = SDL_Rect()

        cursor_dest_rect.x = int((WindowSize.WIDTH / 2 - 200) - (cursor_size / 2))
        cursor_dest_rect.y = int((WindowSize.HEIGHT / 2 - 72) - (cursor_size / 2)) + (cursor_position[1] * 32)
        cursor_dest_rect.w = cursor_size
        cursor_dest_rect.h = cursor_size

        self.renderer.clear()

        SDL_RenderCopy(renderer, menu_bg.texture, None, bg_dest_rect)

        self.menu_dialog.draw(menu_text)

        SDL_RenderCopy(renderer, menu_cursor.texture, None, cursor_dest_rect)

        self.renderer.present()

    def launch_debug(self):
        game = Game(self.window, self.renderer)
        game.run()

        self.running = True
        self.run()
