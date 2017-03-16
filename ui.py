# coding=utf-8

from sdl2 import SDL_ClearError, \
    SDL_CreateTextureFromSurface, \
    SDL_CreateRGBSurface, \
    SDL_FreeSurface, \
    SDL_RenderCopy, \
    SDL_Rect, \
    SDL_Color, \
    SDL_DestroyTexture, \
    SDL_SWSURFACE, \
    SDL_BlitSurface

from sdl2.sdlttf import TTF_Init, \
    TTF_RenderText_Blended, \
    TTF_OpenFont, \
    TTF_CloseFont, \
    TTF_GetError, \
    TTF_RenderText_Shaded

from sdl2.ext import Resources, \
    TextureSpriteRenderSystem, \
    TextureSprite, \
    SoftwareSprite, \
    SoftwareSpriteRenderSystem, \
    SDLError, \
    FontManager, \
    load_image, \
    subsurface

from const import Colors
from utils import count_chars

RESOURCES = Resources(__file__, 'resources', 'ui')
FONTS = Resources(__file__, 'resources', 'fonts')


class SoftSprite(SoftwareSprite):
    def __init__(self, renderer, font=None, text="", font_size=16,
                 text_color=SDL_Color(255, 255, 255),
                 background_color=SDL_Color(0, 0, 0)):

        self.renderer = renderer

        if font is None:
            font = FONTS.get_path("04B_20__.TTF")
        else:
            font = FONTS.get_path(font)

        self.font_manager = FontManager(font, bg_color=background_color)

        self._text = text
        self.font_size = font_size
        self.text_color = text_color
        self.background_color = background_color

        surface = self._create_surface()

        super(SoftSprite, self).__init__(surface, True)

    def _create_surface(self):
        surface = self.font_manager.render(self._text)
        if surface is None:
            raise TTF_GetError()
        return surface

    def _update_surface(self):

        surface = self._create_surface()
        super(SoftSprite, self).__init__(surface, None)

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        if self._text == value:
            return
        self._text = value

        self._update_surface()


class TextSprite(TextureSprite):
    def __init__(self, renderer, font=None, text="", font_size=16,
                 text_color=SDL_Color(255, 255, 255),
                 background_color=SDL_Color(0, 0, 0)):

        self.renderer = renderer

        if font is None:
            font = FONTS.get_path("04B_20__.TTF")
        else:
            font = FONTS.get_path(font)

        self.font = TTF_OpenFont(font.encode("UTF-8"), font_size)

        if self.font is None:
            raise TTF_GetError()
        self._text = text
        self.font_size = font_size
        self.text_color = text_color
        self.background_color = background_color
        texture = self._create_texture()

        super(TextSprite, self).__init__(texture)

    def _create_texture(self):
        text_surface = TTF_RenderText_Shaded(self.font, self._text.encode("UTF-8"), self.text_color,
                                             self.background_color)
        if text_surface is None:
            raise TTF_GetError()

        texture = SDL_CreateTextureFromSurface(self.renderer, text_surface)

        if texture is None:
            raise SDLError()

        SDL_FreeSurface(text_surface)
        return texture

    def _update_texture(self):
        texture_to_delete = self.texture

        texture = self._create_texture()
        super(TextSprite, self).__init__(texture)

        SDL_DestroyTexture(texture_to_delete)

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        if self._text == value:
            return
        self._text = value

        self._update_texture()


class Dialog:
    def __init__(self, factory, *args, **kwargs):
        self.position = kwargs['position']

        self.dialog_box = DialogBox(factory, *args, **kwargs)

        self.lines = self.dialog_box.lines
        self.font_size = self.dialog_box.font_size

        self.text = self.dialog_box.get_sprites()

        self.decoration = DialogDecorations(self.lines, self.font_size)
        self.decoration.position = self.position[0] - 32, self.position[1] - 32

    def get_decoration_sprites(self):
        return self.decoration

    def get_text_sprites(self):
        return self.text


class DialogDecorations(SoftwareSprite):
    def __init__(self, lines, font_size):

        self.free = True

        border_sprite_sheet_path = RESOURCES.get_path("dialog_border.png")
        self.border_sprite_sheet = load_image(border_sprite_sheet_path)

        self.surface = self.create_surface(lines, font_size)

        super(DialogDecorations, self).__init__(self.surface.contents, self.free)

    def create_surface(self, lines, font_size):

        max_chars = 8
        tile_size = 16
        offset = tile_size * 4

        width = font_size * max_chars
        height = font_size * lines

        surface = SDL_CreateRGBSurface(SDL_SWSURFACE,
                                       width + offset,
                                       height + offset,
                                       32,
                                       0x000000FF,
                                       0x0000FF00,
                                       0x00FF0000,
                                       0xFF000000)

        cols = int(width / tile_size) + 3
        rows = int(height / tile_size) + 3

        sprite_crop = [0, 0, tile_size, tile_size]

        for i in range(cols + 1):
            for j in range(rows + 1):
                if (i == 0) and (j == 0):
                    sprite_crop[0] = 0
                    sprite_crop[1] = 0
                elif (i < cols) and (j == 0):
                    sprite_crop[0] = 16
                    sprite_crop[1] = 0
                elif (i == cols) and (j == 0):
                    sprite_crop[0] = 32
                    sprite_crop[1] = 0
                elif (i == cols) and (j < rows):
                    sprite_crop[0] = 32
                    sprite_crop[1] = 16
                elif (i == 0) and (j < rows):
                    sprite_crop[0] = 0
                    sprite_crop[1] = 16
                elif (i == 0) and (j == rows):
                    sprite_crop[0] = 0
                    sprite_crop[1] = 32
                elif (i < cols) and (j == rows):
                    sprite_crop[0] = 16
                    sprite_crop[1] = 32
                elif (i == cols) and (j == rows):
                    sprite_crop[0] = 32
                    sprite_crop[1] = 32
                else:
                    sprite_crop[0] = 16
                    sprite_crop[1] = 16

                rect = SDL_Rect((16 * i), (16 * j))
                tile = subsurface(self.border_sprite_sheet, sprite_crop)
                SDL_BlitSurface(tile, None, surface, rect)

        return surface


class DialogBox:
    def __init__(self, factory, *args, **kwargs):

        self.factory = factory

        self.font_size = kwargs['font_size']
        self.fg_color = kwargs['fg_color']
        self.bg_color = kwargs['bg_color']
        self.font_name = kwargs['font_name']
        self.text = kwargs['text']
        self.position = kwargs['position']
        self.renderer = kwargs['renderer']

        self.sprites = []
        self.surface = None

        self.lines = len(self.text.items())

        for i in range(self.lines):
            self.create_text_sprites(i)

        super(DialogBox, self).__init__()

    def create_text_sprites(self, line):

        text_sprite = None

        if isinstance(self.renderer, SoftwareSpriteRenderSystem):
            text_sprite = SoftSprite(self.renderer, self.font_name, self.text[line],
                                     font_size=self.font_size,
                                     text_color=self.fg_color,
                                     background_color=self.bg_color)

        elif isinstance(self.renderer, TextureSpriteRenderSystem):
            text_sprite = TextSprite(self.renderer, self.font_name, self.text[line],
                                     font_size=self.font_size,
                                     text_color=self.fg_color,
                                     background_color=self.bg_color)

        text_sprite.x = self.position[0]
        text_sprite.y = self.position[1] + (self.font_size * line)

        self.sprites.append(text_sprite)

    def get_sprites(self):
        return self.sprites
