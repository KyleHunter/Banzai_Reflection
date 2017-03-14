from Internal.Reflection import *
from Core.Globals import *
import re
from Internal.Cache.CacheLoader import *

class TPoint():
    def __init__(self, x=-1, y=-1):
        self.x, self.y = x, y


def get_setting_array():
    return [get_int_array(STATIC_OBJECT, Client_GameSettings, i) for i in range(0, 2000)]


def get_setting(setting):
    return get_int_array(STATIC_OBJECT, Client_GameSettings, setting)


def get_client_loop_cycle():
    return get_int(STATIC_OBJECT, Client_LoopCycle)


def get_base_x():
    return get_int(STATIC_OBJECT, Client_BaseX)


def get_base_y():
    return get_int(STATIC_OBJECT, Client_BaseY)


def get_cache_entry(id, entry, cache_type='item'):
    if cache_type == 'npc':
        return re.search('%s(.*)%s' % ('"' + entry + '": "', '",'), cache.npcs[id]).group(1)
    if cache_type == 'item':
        return re.search('%s(.*)%s' % ('"' + entry + '": "', '",'), cache.items[id]).group(1)
    if cache_type == 'object':
        return re.search('%s(.*)%s' % ('"' + entry + '": "', '",'), cache.objects[id]).group(1)
