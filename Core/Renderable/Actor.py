"""
*   Actor.py contains methods common to all actor classes
*
*   Actor should never be directly called, only extended into another class, i.e npcs
"""
import Misc.Misc as Misc
import Internal.Reflection as Ref
import Internal.Hooks as Hook


class Actor:
    def get_spoken_text(self):
        temp = []
        for i in self.results:
            temp.append(Misc.get_string(i, Hook.Actor_SpokenText))
        return temp

    def get_tile(self):
        temp = []
        for i in self.results:
            temp.append(Misc.TPoint(round(Misc.get_base_x() + Ref.get_int(i, Hook.Actor_WorldX) /
                                          128), round(Misc.get_base_y() + Ref.get_int(i, Hook.Actor_WorldY) / 128)))
        return temp

    def get_queue_size(self):
        temp = []
        for i in self.results:
            temp.append(Ref.get_int(i, Hook.Actor_QueueSize))
        return temp

    def get_animation(self):
        temp = []
        for i in self.results:
            temp.append(Ref.get_int(i, Hook.Actor_Animation))
        return temp
