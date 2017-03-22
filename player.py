# -*- coding: utf-8 -*-

from sdl2.ext import Resources, \
    Entity

from components.frames import Frames
from components.motion import MotionType
from components.facing import Facing

# from spell import Spell
# from inventory import Inventory

from components.velocity import Velocity

RESOURCES = Resources(__file__, 'resources')


class Player(Entity):
    def __init__(self, world, sprite, posx=0, posy=0):
        super(Player, self).__init__()

        self.sprite = sprite
        self.sprite.position = posx, posy

        self.frames = Frames()
        self.motiontype = MotionType()
        self.facing = Facing()
        self.velocity = Velocity()

        self.playerdata = PlayerData()


class PlayerData:
    def __init__(self):
        super(PlayerData, self).__init__()
        self.life = 100
