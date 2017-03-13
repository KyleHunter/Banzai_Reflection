from ctypes import *


#  HELPERS
def string_to_char_p(s):
    return c_char_p(s.encode('utf-8'))


#  STRUCTS
class SHMemData(Structure):
    _fields_ = [("port", c_int), ("id", c_int), ("width", c_int), ("height", c_int), ("paired", c_bool),
                ("imgoff", c_int), ("dbgoff", c_int), ("args", c_char * 4096)]


class SMARTClient(Structure):
    _fields_ = [("width", c_int), ("height", c_int), ("refcount", c_int), ("socket", c_int), ("fd", c_int),
                ("memmap", c_void_p), ("data", POINTER(SHMemData))]


class RGBA(Structure):
    _fields_ = [("b", c_ubyte), ("g", c_ubyte), ("r", c_ubyte), ("a", c_ubyte)]


class RGB(Union):
    _fields_ = [("rgba", RGBA), ("colour", c_int32)]


class Point:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y


class Size:
    def __init__(self, width=0, height=0):
        self.width = width
        self.height = height


def get_overflow(int_val):
    temp = int_val & 0xffffffff
    if temp == 0xffffffff:
        return -1
    else:
        return temp
