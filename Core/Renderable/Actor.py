"""
*   Actor.py contains methods common to all actor classes
*
*   Actor should never be directly called, only extended into another class, i.e npcs
"""
from Internal.Reflection import *
from Internal.Hooks import *
from Core.Globals import *
from Misc.Misc import *


class Actor:
    def get_spoken_text(self):
        temp = []
        for i in self.results:
            temp.append(get_string(i, Actor_SpokenText))
        return temp

    def get_tile(self):
        temp = []
        for i in self.results:
            temp.append(TPoint(round(get_base_x() + get_int(i, Actor_WorldX) /
                                     128), round(get_base_y() + get_int(i, Actor_WorldY) / 128)))
        return temp

    def get_queue_size(self):
        temp = []
        for i in self.results:
            temp.append(get_int(i, Actor_QueueSize))
        return temp

    def get_animation(self):
        temp = []
        for i in self.results:
            temp.append(get_int(i, Actor_InteractingIndex))
        return temp
