"""
*   Npcs.py contains all methods unique to npcs
*
*   Pending changes
"""
from Core.Renderable.Actor import Actor
import Internal.Smart as Smart
import Internal.Reflection as Ref
import Internal.Hooks as Hook
import Core.Globals as Global
import Misc.Misc as Misc


class Npcs(Actor):
    def __init__(self, name='', id=-1, distance=-1):
        self._object_refs, self.results = [], []
        for i in self.get_indices():
            self._object_refs.append(Ref.get_object_array(Global.STATIC_OBJECT, Hook.Client_LocalNpcs, i))
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
            Smart.smart_instance.free_object(Smart.smart_instance.target, i)

    @staticmethod
    def get_indices():
        return [Ref.get_int_array(Global.STATIC_OBJECT, Hook.Client_NpcIndices, i)
                for i in range(0, Ref.get_int(Global.STATIC_OBJECT, Hook.Client_NpcIndices_Size))]

    def get_id(self):
        temp = []
        for obj in self.results:
            with Ref.RefObject(obj, Hook.Npc_Definition)as npc_def:
                temp.append(Ref.get_int(npc_def.reference, Hook.NpcDefinition_ID))
        return temp

    def get_name(self):
        temp = []
        for i in self.get_id():
            temp.append(Misc.get_cache_entry(i, 'name', 'npc'))
        return temp
