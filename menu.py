# -*- coding: utf-8 -*-

from sdl2 import SDL_Delay,\
    SDL_GetTicks,\
    SDL_KEYDOWN,\
    SDL_KEYUP,\
    SDL_QUIT,\
    SDL_Rect,\
    SDL_RenderCopy,\
    SDLK_ESCAPE,\
    SDLK_UP,\
    SDLK_DOWN,\
    SDLK_RETURN,\
    SDL_Quit

from sdl2.ext import Resources,\
    get_events

from const import WindowSize, Colors
from input import Input
from ui import DialogBox
from game import Game

FPS = 60  # units.FPS
MAX_FRAME_TIME = int(5 * (1000 / FPS))
RESOURCES = Resources(__file__, 'resources')


class Menu:
    def __init__(self, window, world, renderer, factory):
        self.window = window
        self.renderer = renderer
        self.world = world
        self.factory = factory

        self.rsystem = factory.create_sprite_render_system(window)

        self.menu_bg = RESOURCES.get_path("menu_bg.png")
        self.menu_cursor = RESOURCES.get_path("menu_cursor.png")

        self.running = True
        self.position = 460, 340
        self.cursor_start_position = 370, 330
        self.cursor_position = 0
        self.cursor_sprite_size = 32

        self.background_sprite = self.factory.from_image(self.menu_bg)
        self.cursor_sprite = self.factory.from_image(self.menu_cursor)

        self.text = {0: "START",
                     1: "OPTIONS",
                     2: "EXIT"}

        self.dialog = DialogBox(self.factory,
                                font_size=32,
                                fg_color=Colors.WHITE,
                                bg_color=Colors.BLACK,
                                font_name="04B_20__.TTF",
                                text=self.text,
                                position=self.position,
                                renderer=self.renderer)

        self.sprites = [self.background_sprite]

        sprites = self.dialog.get_sprites()

        for sprite in sprites:
            self.sprites.append(sprite)

        self.sprites.append(self.cursor_sprite)

    def __del__(self):
        SDL_Quit()

    def update(self, elapsed_time):
        self.cursor_sprite.position = self.cursor_start_position[0], self.cursor_start_position[1] \
                                      + self.cursor_position * self.cursor_sprite_size

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
                if self.cursor_position != 0:
                    self.cursor_position -= 1
            elif menu_input.was_key_pressed(SDLK_DOWN):
                if self.cursor_position != 2:
                    self.cursor_position += 1

            # Select option
            elif menu_input.was_key_pressed(SDLK_RETURN):
                self.running = False
                if self.cursor_position == 0:
                    self.launch_game()

            current_time = SDL_GetTicks()  # units.MS
            elapsed_time = current_time - last_update_time  # units.MS

            self.update(min(elapsed_time, MAX_FRAME_TIME))

            last_update_time = current_time

            self.renderer.render(self.sprites)

            # This loop lasts 1/60th of a second, or 1000/60th ms
            ms_per_frame = 1000 // FPS  # units.MS
            elapsed_time = SDL_GetTicks() - start_time  # units.MS
            if elapsed_time < ms_per_frame:
                SDL_Delay(ms_per_frame - elapsed_time)

    def launch_game(self):
        game = Game(self.world, self.window, self.renderer, self.factory)
        game.run()

        self.running = True
        self.run()
