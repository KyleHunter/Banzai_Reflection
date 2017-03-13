from Core.Renderable.Actor import *
from Internal.Cache.CacheLoader import cache
from Internal.Reflection import *


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

    def __enter__(self, name='', id=-1, distance=-1):
        return self

    def __exit__(self, type, value, traceback):
        for i in self._object_refs:
            smart_instance.free_object(smart_instance.target, i)

    def get_indices(self):
        return [get_int_array(STATIC_OBJECT, Client_NpcIndices, i)
                for i in range(0, get_int(0, Client_NpcIndices_Size))]

    def get_id(self):
        temp = []
        for obj in self._object_refs:
            with RefObject(obj, Npc_Definition)as npc_def:
                temp.append(get_int(npc_def.reference, NpcDefinition_ID))
        return temp

    def get_name(self):
        import re
        temp = []
        for i in self.get_id():
            if re.search('%s(.*)%s' % ('"name": "', '",'), cache.npcs[i]) is None:
                continue
            temp.append(re.search('%s(.*)%s' % ('"name": "', '",'), cache.npcs[i]).group(1))
        return temp
