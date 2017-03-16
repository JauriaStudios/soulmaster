# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Filename:    db.py
# Created:     03/16/2017
# Author:      TurBoss
# E-mail:      j.l.toledano.l@gmail.com
# License:     GNU GPL 3.0
# ---------------------------------------------------------------------------

""" Database Wrapper """

import sqlite3

from sdl2.ext import Resources

from utils import dict_factory

DB = Resources(__file__, 'resources', 'db')


class DataBase:
    """" Functions to get and set the database """
    def __init__(self):
        """ Get the database path """
        self.db_path = DB.get_path('database.sqlite')

    def get_all_npc(self):
        """
        Get all NPC from the database

        :rtype dict
        :returns all npc in the database
        """
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = dict_factory
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM npc')
            query = cursor.fetchall()

        return query

    def get_npc(self, name):
        """
        Get NPC attributes from the database based on its name

        :param name npc name
        :rtype dict
        :returns return all attributes from the given npc
        """
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = dict_factory
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM npc WHERE name = ?', (name,))
            query = cursor.fetchone()

        return query

    def get_npc_dialog(self, name):
        """
        Get all NPC dialogs from the database based on its name
        :param name npc name
        :rtype dict
        :returns all dialog for the given npc
        """
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = dict_factory
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM dialogs WHERE npc = ?', (name,))
            query = cursor.fetchall()

        return query

    def get_map_npc(self, map_name):
        """
        Get all NPC from a map based on the map name
        :param map_name map name
        :rtype dict
        :returns all the npc from the given map
        """
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = dict_factory
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM map WHERE name = ?', (map_name,))
            query = cursor.fetchall()

        return query

    def get_player_inventory(self):
        """
        Get all the items the player has on its inventory, equip and stash
        :rtype dict
        :returns all the player items
        """
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = dict_factory
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM inventory')
            query = cursor.fetchone()

        return query

    def get_item_by_id(self, item_id):
        """
        Get all properties of an item based on its ID
        :param item_id item ID
        :rtype dict
        :returns all the properties of the given item
        """
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = dict_factory
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM items WHERE id = ?', (item_id,))
            query = cursor.fetchone()

        return query
