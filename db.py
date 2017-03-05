# -*- coding: utf-8 -*-

import os
import sys
import sqlite3

# If we're on Windows, use the included compiled DLLs.
if sys.platform == "win32":
    os.environ["PYSDL2_DLL_PATH"] = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'libs')

from sdl2 import *
import sdl2.ext

from utils import dict_factory

DB = sdl2.ext.Resources(__file__, 'resources', 'db')


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

