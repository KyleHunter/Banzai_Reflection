"""
*   Actor.py contains methods common to all actor classes
*
*   Actor should never be directly called, only extended into another class, i.e npcs
"""
from Internal.Reflection import *
from Internal.Hooks import *
from Core.Globals import *


class Actor:

    def get_spoken_text(self):
        temp = []
        for i in self._object_refs:
            temp.append(get_string(i, Actor_SpokenText))
        return temp

    def get_queue_size(self):
        temp = []
        for i in self._object_refs:
            temp.append(get_int(i, Actor_QueueSize))
        return temp

    def get_animation(self):
        temp = []
        for i in self._object_refs:
            temp.append(get_int(i, Actor_InteractingIndex))
        return temp
