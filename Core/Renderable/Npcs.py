"""
*   Npcs.py contains all methods unique to npcs
*
*   Pending changes
"""
from Core.Renderable.Actor import *
from Internal.Cache.CacheLoader import cache
from Internal.Reflection import *
from Misc.Misc import *
import re


class Npcs(Actor):
    def __init__(self, name='', id=-1, distance=-1):
        self._object_refs, self.results = [], []
        for i in self.get_indices():
            self._object_refs.append(get_object_array(STATIC_OBJECT, Client_LocalNpcs, i))
        self.results = self._object_refs

        temp, h = [], 0
        if name != '':
            for s in self.get_name():
                if s == name:
                    temp.append(h)
                h += 1
        self.results = [self._object_refs[t] for t in temp]

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        for i in self._object_refs:
            smart_instance.free_object(smart_instance.target, i)

    @staticmethod
    def get_indices():
        return [get_int_array(STATIC_OBJECT, Client_NpcIndices, i)
                for i in range(0, get_int(0, Client_NpcIndices_Size))]

    def get_id(self):
        temp = []
        for obj in self.results:
            with RefObject(obj, Npc_Definition)as npc_def:
                temp.append(get_int(npc_def.reference, NpcDefinition_ID))
        return temp

    def get_name(self):
        temp = []
        for i in self.get_id():
            temp.append(get_cache_entry(i, 'name', 'npc'))
        return temp
