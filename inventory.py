# -*- coding: utf-8 -*-

import json

from sdl2.ext import Resources

from const import Colors
from ui import DialogBox
from db import DataBase

RESOURCES = Resources(__file__, 'resources', 'ui')


class Inventory:
    def __init__(self, window, renderer):

        self.db = DataBase()

        self.window = window
        self.renderer = renderer

        self.inventory = self.db.get_player_inventory()
        self.equipped = json.loads(self.inventory["equipped"])
        self.left_hand_id = self.equipped["left_hand"]
        self.left_hand = self.db.get_item_by_id(self.left_hand_id)
        print(self.left_hand)

        self.inv_text = {0: self.left_hand["name"], 1: self.left_hand["description"]}
        self.inv_dialog = DialogBox(self.window, self.renderer, Colors.WHITE, 16, (300, 200), Colors.BLACK, "GlametrixBold.otf")

    def update(self, elapsed_time):
        pass

    def draw(self):
        inv_text = self.inv_text

        self.inv_dialog.draw(inv_text)
