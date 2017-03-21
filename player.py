# -*- coding: utf-8 -*-

from sdl2.ext import Resources, \
    Entity

from components.spritesheet import SpriteSheet
from components.frames import Frames
from components.motion import MotionType
from components.facing import Facing

from spell import Spell
from inventory import Inventory

from components.velocity import Velocity

RESOURCES = Resources(__file__, 'resources')


class Player(Entity):
    def __init__(self, world, posx=0, posy=0):

        self.sprite = SpriteSheet().get_sprite()
        self.sprite.position = posx, posy

        self.frames = Frames()
        self.motion_types = MotionType()
        self.facing = Facing()

        self.velocity = Velocity()

        self.player_data = PlayerData()


class PlayerData:
    def __init__(self):
        super(PlayerData, self).__init__()
        self.life = 100
