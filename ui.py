# coding=utf-8

from sdl2 import SDL_ClearError, SDL_CreateTextureFromSurface, SDL_FreeSurface, SDL_RenderCopy, SDL_Rect, SDL_Color, \
    SDL_DestroyTexture
from sdl2.sdlttf import TTF_Init, TTF_RenderText_Blended, TTF_OpenFont, TTF_CloseFont, TTF_GetError, \
    TTF_RenderText_Shaded
from sdl2.ext import Resources, TextureSpriteRenderSystem, Entity, TextureSprite, SoftwareSprite, \
    SoftwareSpriteRenderSystem, SDLError, FontManager

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

        self.font_manager = FontManager(font, bg_color=(100, 0, 0))

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
    def __init__(self, sprite):
        super(Dialog, self).__init__()
        self.text = sprite

        self.border_sprites = []

    def decoration_sprites(self):

        max_chars = self.max_chars
        lines = self.lines
        tile_size = 16

        width = self.text_size * max_chars
        height = self.text_size * lines

        x = self.text_position[0]
        y = self.text_position[1]

        background = self.factory.from_color(Colors.BLACK,
                                             size=(width + (tile_size * 2),
                                                   height + (tile_size * 2)))
        background.position = x - tile_size, y - tile_size

        self.border_sprites.append(background)

        cols = int(width / tile_size) + 3
        rows = int(height / tile_size) + 3

        border_crop = [0, 0, tile_size, tile_size]

        for i in range(cols + 1):
            for j in range(rows + 1):
                if (i == 0) and (j == 0):
                    border_crop[0] = 0
                    border_crop[1] = 0
                elif (i < cols) and (j == 0):
                    border_crop[0] = 16
                    border_crop[1] = 0
                elif (i == cols) and (j == 0):
                    border_crop[0] = 32
                    border_crop[1] = 0
                elif (i == cols) and (j < rows):
                    border_crop[0] = 32
                    border_crop[1] = 16
                elif (i == 0) and (j < rows):
                    border_crop[0] = 0
                    border_crop[1] = 16
                elif (i == 0) and (j == rows):
                    border_crop[0] = 0
                    border_crop[1] = 32
                elif (i < cols) and (j == rows):
                    border_crop[0] = 16
                    border_crop[1] = 32
                elif (i == cols) and (j == rows):
                    border_crop[0] = 32
                    border_crop[1] = 32
                else:
                    border_crop[0] = 16
                    border_crop[1] = 16

                sprite = self.window_sprite.subsprite(border_crop)
                sprite.position = (16 * i) + (x - 32), (16 * j) + (y - 32)

                self.border_sprites.append(sprite)

        return self.border_sprites


class DialogBox(Entity):
    def __init__(self, **kwargs):
        if "renderer" not in kwargs:
            raise ValueError("you have to provide a renderer= argument")

        self.font_size = kwargs['font_size']
        self.fg_color = kwargs['fg_color']
        self.bg_color = kwargs['bg_color']
        self.font = kwargs['font']
        self.text = kwargs['text']

        renderer = kwargs['renderer']

        super(DialogBox, self).__init__()

        msg_sprite = None

        if isinstance(renderer, SoftwareSpriteRenderSystem):
            msg_sprite = SoftSprite(renderer, self.font, "TEXT MESSAGE")
        elif isinstance(renderer, TextureSpriteRenderSystem):
            msg_sprite = TextSprite(renderer, self.font, "TEXT MESSAGE")

        self.dialog = Dialog(msg_sprite)

        self.text_sprite = msg_sprite


class DialogBoxOLD:
    def __init__(self, window, renderer, factory, text, text_color, text_size, text_position, font):
        TTF_Init()

        self.window = window
        self.window_size = window.size
        self.renderer = renderer

        self.text = text
        self.text_color = text_color
        self.text_size = text_size
        self.text_position = text_position

        self.lines, self.max_chars = count_chars(self.text)

        self.font_path = FONTS.get_path(font)

        self.image = None

        self.factory = factory

        window_image_path = RESOURCES.get_path("dialog_border.png")
        self.window_sprite = self.factory.from_image(window_image_path)
        self.border_sprites = []

        self.bg = None

    def render_text(self, message, font_file, font_color, font_size):
        SDL_ClearError()
        font = TTF_OpenFont(font_file.encode("UTF-8"), font_size)

        if font is None:
            return None

        surf = TTF_RenderText_Blended(font,
                                      message.encode("UTF-8"),
                                      font_color)

        if surf is None:
            TTF_CloseFont(font)
            return None

        texture = SDL_CreateTextureFromSurface(self.renderer,
                                               surf)

        if texture is None:
            return None

        SDL_FreeSurface(surf)
        TTF_CloseFont(font)

        return texture

    def draw(self, messages, text_position=None):

        renderer = self.renderer

        if text_position:
            self.text_position = text_position

        chars = []
        for (index, text) in messages.items():
            i = 0
            for _ in text:
                i += 1
            chars.append(i)

        max_chars = max(chars)

        width = (self.text_size * max_chars)
        height = self.text_size
        x = self.text_position[0]
        y = self.text_position[1]

        self.decoration_textures()

        for (index, text) in messages.items():
            self.image = self.render_text(text,
                                          self.font_path,
                                          self.text_color,
                                          self.text_size)

            text_dest = SDL_Rect(x, (y + (self.text_size * index)))
            text_dest.w = self.text_size * chars[index]
            text_dest.h = height

            SDL_RenderCopy(renderer,
                           self.image,
                           None,
                           text_dest)

    def decoration_textures(self):

        width = (self.text_size * self.max_chars)
        height = self.text_size
        x = self.text_position[0]
        y = self.text_position[1]

        renderer = self.renderer

        self.bg = self.factory.from_color(Colors.BLACK,
                                          size=(width, height))

        bg_dest = SDL_Rect(x - 16,
                           y - 16,
                           width + 32,
                           height + 32)

        SDL_RenderCopy(renderer,
                       self.bg.texture,
                       None,
                       bg_dest)

        border_src = SDL_Rect(0, 0, 16, 16)
        border_dest = SDL_Rect(0, 0, 16, 16)

        cols = int(width / 16) + 3
        rows = int(height / 16) * chars + 3

        for i in range(cols + 1):
            for j in range(rows + 1):
                if (i == 0) and (j == 0):
                    border_src.x = 0
                    border_src.y = 0
                elif (i < cols) and (j == 0):
                    border_src.x = 16
                    border_src.y = 0
                elif (i == cols) and (j == 0):
                    border_src.x = 32
                    border_src.y = 0
                elif (i == cols) and (j < rows):
                    border_src.x = 32
                    border_src.y = 16
                elif (i == 0) and (j < rows):
                    border_src.x = 0
                    border_src.y = 16
                elif (i == 0) and (j == rows):
                    border_src.x = 0
                    border_src.y = 32
                elif (i < cols) and (j == rows):
                    border_src.x = 16
                    border_src.y = 32
                elif (i == cols) and (j == rows):
                    border_src.x = 32
                    border_src.y = 32
                else:
                    border_src.x = 16
                    border_src.y = 16

                border_dest.x = (16 * i) + (x - 32)
                border_dest.y = (16 * j) + (y - 32)

                SDL_RenderCopy(renderer,
                               self.border.texture,
                               border_src,
                               border_dest)

    def decoration_sprites(self):

        max_chars = self.max_chars
        lines = self.lines
        tile_size = 16

        width = self.text_size * max_chars
        height = self.text_size * lines

        x = self.text_position[0]
        y = self.text_position[1]

        background = self.factory.from_color(Colors.BLACK,
                                             size=(width + (tile_size * 2),
                                                   height + (tile_size * 2)))
        background.position = x - tile_size, y - tile_size

        self.border_sprites.append(background)

        cols = int(width / tile_size) + 3
        rows = int(height / tile_size) + 3

        border_crop = [0, 0, tile_size, tile_size]

        for i in range(cols + 1):
            for j in range(rows + 1):
                if (i == 0) and (j == 0):
                    border_crop[0] = 0
                    border_crop[1] = 0
                elif (i < cols) and (j == 0):
                    border_crop[0] = 16
                    border_crop[1] = 0
                elif (i == cols) and (j == 0):
                    border_crop[0] = 32
                    border_crop[1] = 0
                elif (i == cols) and (j < rows):
                    border_crop[0] = 32
                    border_crop[1] = 16
                elif (i == 0) and (j < rows):
                    border_crop[0] = 0
                    border_crop[1] = 16
                elif (i == 0) and (j == rows):
                    border_crop[0] = 0
                    border_crop[1] = 32
                elif (i < cols) and (j == rows):
                    border_crop[0] = 16
                    border_crop[1] = 32
                elif (i == cols) and (j == rows):
                    border_crop[0] = 32
                    border_crop[1] = 32
                else:
                    border_crop[0] = 16
                    border_crop[1] = 16

                sprite = self.window_sprite.subsprite(border_crop)
                sprite.position = (16 * i) + (x - 32), (16 * j) + (y - 32)

                self.border_sprites.append(sprite)

        return self.border_sprites
