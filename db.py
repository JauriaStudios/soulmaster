# -*- coding: utf-8 -*-

import sqlite3

from sdl2.ext import Resources

from utils import dict_factory

DB = Resources(__file__, 'resources', 'db')


class DataBase:
    def __init__(self):
        self.db_path = DB.get_path('database.sqlite')

    def get_all_npc(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = dict_factory
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM npc')
            query = cursor.fetchall()

        return query

    def get_npc(self, name):
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = dict_factory
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM npc WHERE name = ?', (name,))
            query = cursor.fetchone()

        return query

    def get_npc_dialog(self, name):
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = dict_factory
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM dialogs WHERE npc = ?', (name,))
            query = cursor.fetchall()

        return query

    def get_map_npc(self, map):
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = dict_factory
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM map WHERE name = ?', (map,))
            query = cursor.fetchall()

        return query
