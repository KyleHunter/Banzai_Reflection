import Internal.Reflection as Ref
import Core.Globals as Global
import Internal.Hooks as Hook
import Internal.Cache.CacheLoader as Cl
import re


class TPoint:
    def __init__(self, x=-1, y=-1):
        self.x, self.y = x, y


def get_setting_array():
    return [Ref.get_int_array(Global.STATIC_OBJECT, Hook.Client_GameSettings, i) for i in range(0, 2000)]


def get_setting(setting):
    return Ref.get_int_array(Global.STATIC_OBJECT, Hook.Client_GameSettings, setting)


def get_client_loop_cycle():
    return Ref.get_int(Global.STATIC_OBJECT, Hook.Client_LoopCycle)


def get_base_x():
    return Ref.get_int(Global.STATIC_OBJECT, Hook.Client_BaseX)


def get_base_y():
    return Ref.get_int(Global.STATIC_OBJECT, Hook.Client_BaseY)


def get_cache_entry(id, entry, cache_type='item'):
    try:
        if cache_type == 'npc':
            return re.search('%s(.*)%s' % ('"' + entry + '": "', '",'), Cl.cache.npcs[id]).group(1)
        if cache_type == 'item':
            return re.search('%s(.*)%s' % ('"' + entry + '": "', '",'), Cl.cache.items[id]).group(1)
        if cache_type == 'object':
            return re.search('%s(.*)%s' % ('"' + entry + '": "', '",'), Cl.cache.objects[id]).group(1)
    except AttributeError:
        pass
