# -*- coding: utf-8 -*-

from sdl2.ext import Resources, \
    Entity

from components.frames import Frames
from components.motion import MotionType
from components.facing import Facing

from components.velocity import Velocity

RESOURCES = Resources(__file__, 'resources')


class Npc(Entity):
    def __init__(self, world, sprite, posx=0, posy=0):
        super(Npc, self).__init__()

        self.sprite = sprite
        self.sprite.position = posx, posy

        self.frames = Frames()
        self.motiontype = MotionType()
        self.facing = Facing()
        self.velocity = Velocity()

        self.npcdata = NpcData()


class NpcData:
    def __init__(self):
        super(NpcData, self).__init__()

        self.ai = True
        self.ally = True

        self.life = 100


"""
class MotionType:
    STANDING = 0
    WALKING = 1
    COUNT = 2


class Facing:
    LEFT_DOWN = 0
    DOWN = 1
    RIGHT_DOWN = 2
    RIGHT = 3
    RIGHT_UP = 4
    UP = 5
    LEFT_UP = 6
    LEFT = 7
    COUNT = 8


class NPC:
    def __init__(self, renderer, factory, json_data):

        self.dialog_timer = Timer(10000)
        self.close_dialog_timer = Timer(10000)

        self.db = DataBase()

        self.renderer = renderer
        self.factory = factory

        data = json.loads(json_data)

        self.name = data["name"]
        self.start_pos = data["start_pos"]

        self.npc_data = self.db.get_npc(self.name)

        self.level = self.npc_data["level"]
        self.quest = self.npc_data["quest"]
        self.sprite_size = 128
        self.position = [0, 0]
        self.movement = [0, 0]

        self.moving = False

        self.npc_sprites = [
            RESOURCES.get_path("{0}_standing.png".format(self.name)),
            RESOURCES.get_path("{0}_walking.png".format(self.name))
        ]

        self.sprite_sheets = {}
        self.sprites = []

        self.facing = Facing.LEFT_DOWN
        self.last_facing = self.facing

        self.motion_type = MotionType.STANDING
        self.last_motion_type = self.motion_type

        self.frame_index = 0
        self.walk_frames = 60
        self.move_rate = 100

        self.init_sprite_sheet()

        self.dialogs = self.db.get_npc_dialog(self.name)
        self.dialog_box = None
        self.dialog_sprites = []
        self.text = None

    def init_sprite_sheet(self):
        for motion_type in range(MotionType.COUNT):
            self.load_image(self.npc_sprites[motion_type], motion_type)

    def load_image(self, file_path, motion_type):
        sprite_sheets = self.sprite_sheets.get(file_path)
        if not sprite_sheets:
            sprite_surface = self.factory.from_image(file_path)
            self.sprite_sheets[motion_type] = sprite_surface

    def update(self, position, elapsed_time):

        self.position = position
        self.sprites.clear()
        self.frame_index += 1

        if self.frame_index == (self.sprite_sheets[self.motion_type].size[0] / self.sprite_size):
            self.frame_index = 0

        if not self.moving:
            move = dice(self.move_rate)
            if move[0] == self.move_rate - 1:
                self.moving = True
                self.walk_frames = 60
                facing = dice(Facing.COUNT - 1)
                self.facing = facing[0]

        if self.moving:
            if self.walk_frames:
                self.motion_type = MotionType.WALKING

                if self.facing == 0:
                    self.movement[0] -= 2
                    self.movement[1] += 1
                    self.facing = Facing.LEFT_DOWN
                elif self.facing == 1:
                    self.movement[1] += 1
                    self.facing = Facing.DOWN
                elif self.facing == 2:
                    self.movement[0] += 2
                    self.movement[1] += 1
                    self.facing = Facing.RIGHT_DOWN
                elif self.facing == 3:
                    self.movement[0] += 2
                    self.facing = Facing.RIGHT
                elif self.facing == 4:
                    self.movement[0] += 2
                    self.movement[1] -= 1
                    self.facing = Facing.RIGHT_UP
                elif self.facing == 5:
                    self.movement[1] -= 1
                    self.facing = Facing.UP
                elif self.facing == 6:
                    self.movement[0] -= 2
                    self.movement[1] -= 1
                    self.facing = Facing.LEFT_UP
                elif self.facing == 7:
                    self.movement[0] -= 2
                    self.facing = Facing.LEFT

                self.walk_frames -= 1
            else:
                self.moving = False
                self.motion_type = MotionType.STANDING

        x = int((int(self.start_pos[0]) + self.position[0] + self.movement[0]) - (self.sprite_size / 2))
        y = int((int(self.start_pos[1]) + self.position[1] + self.movement[1]) - (self.sprite_size / 2))

        self.position = x, y

        sprite_sheet = self.sprite_sheets[self.motion_type]

        sprite_crop = [self.frame_index * self.sprite_size,
                       self.facing * self.sprite_size,
                       self.sprite_size,
                       self.sprite_size]

        sprite = sprite_sheet.subsprite(sprite_crop)
        sprite.position = self.position

        self.sprites.append(sprite)

    def get_sprites(self):
        return self.sprites

    def dialog_update(self):

        self.dialog_timer.update()
        self.close_dialog_timer.update()

        if self.dialog_timer.check():
            self.dialog_timer.reset()
            self.close_dialog_timer.activate()

            self.create_dialog()

        if self.close_dialog_timer.check():
            self.close_dialog_timer.reset()
            self.dialog_timer.activate()
            self.dialog_box = None
            self.dialog_sprites.clear()

    def create_dialog(self):

        self.text = dice(len(self.dialogs) - 1)

        name = self.dialogs[self.text[0]]['npc']
        text = self.dialogs[self.text[0]]['text']
        message = {0: "{0}:".format(name)}

        max_chars = 24
        i = 1
        for j in range(0, len(text), max_chars):
            message[i] = text[j:j + max_chars]
            i += 1

        self.dialog_box = DialogBox(self.factory,
                                    font_size=32,
                                    fg_color=Colors.WHITE,
                                    bg_color=Colors.BLACK,
                                    font_name="04B_20__.TTF",
                                    text=message,
                                    position=self.position,
                                    renderer=self.renderer)

        sprites = self.dialog_box.get_sprites()
        for sprite in sprites:
            self.dialog_sprites.append(sprite)
"""