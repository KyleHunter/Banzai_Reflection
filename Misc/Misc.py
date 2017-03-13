from Internal.Reflection import *
from Core.Globals import *


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
