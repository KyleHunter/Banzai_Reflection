"""
*   Reflection.py contains all reflection wrappers to be used in library
*
*   RefClasses should be used with context managers always
*
*   Other wrappers only used within context manager classes
"""
from Smart import *
from Misc import *


class RefObject:
    def __init__(self, obj, hook):
        self.obj = obj
        self.field = hook[0]

    def __enter__(self):
        self.reference = smart_instance.get_field_object(smart_instance.target, self.obj, self.field)
        return self

    def __exit__(self, type, value, traceback):
        smart_instance.free_object(smart_instance.target, self.reference)


class RefObjectArray:
    def __init__(self, hook, index):
        self.field = hook[0]
        self.index = index

    def __enter__(self):
        self.object = smart_instance.get_field_array_object(smart_instance.target, 0, self.field, self.index)
        return self

    def __exit__(self, type, value, traceback):
        smart_instance.free_object(smart_instance.target, self.object)


def get_object(obj, hook):
    return smart_instance.smart.exp_getFieldObject(smart_instance.target, obj, hook[0])


def is_hook_valid(obj, hook):
    return smart_instance.smart.exp_ishookValid(smart_instance.target, obj, hook[0])


def get_boolean(obj, hook):
    return smart_instance.smart.exp_getFieldBoolean(smart_instance.target, obj, hook[0])


def get_long_h(obj, hook):
    return smart_instance.smart.exp_getFieldLongH(smart_instance.target, obj, hook[0])


def get_field_long_l(obj, hook):
    return smart_instance.smart.exp_getFieldLongL(smart_instance.target, obj, hook[0])


def get_int(obj, hook):
    return get_overflow(smart_instance.get_field_int(smart_instance.target, obj, hook[0]) * hook[1])


def get_short(obj, hook):

    return smart_instance.smart.exp_getFieldShort(smart_instance.target, obj, hook[0])


def get_float(obj, hook):
    return smart_instance.smart.exp_getFieldFloat(smart_instance.target, obj, hook[0])


def get_double(obj, hook):
    return smart_instance.smart.exp_getFieldDouble(smart_instance.target, obj, hook[0])


def get_byte(obj, hook):
    return smart_instance.smart.exp_getFieldByte(smart_instance.target, obj, hook[0])


def get_array_3d_object(obj, hook, x, y, z):
    return smart_instance.get_field_array_3d_object(smart_instance.target, obj, hook[0], x, y, z)


def get__array_3d_char(obj, hook, x, y, z):
    return smart_instance.get_field_array_3d_char(obj, hook[0], x, y, z)


def get_array_3d_short(obj, hook, x, y, z):
    return smart_instance.get_field_array_3d_short(obj, hook[0], x, y, z)


def get_array_3d_int(obj, hook, x, y, z):
    return smart_instance.get_field_array_3d_int(obj, hook[0], x, y, z)


def get_array_3d_float(obj, hook, x, y, z):
    return smart_instance.get_field_array_3d_float(obj, hook[0], x, y, z)


def get_array_3d_double(obj, hook, x, y, z):
    return smart_instance.get_field_array_3d_double(obj, hook[0], x, y, z)


def get_array_3d_bool(obj, hook, x, y, z):
    return smart_instance.get_field_array_3d_bool(obj, hook[0], x, y, z)


def get_array_3d_long_h(obj, hook, x, y, z):
    return smart_instance.get_field_array_3d_long_h(obj, hook[0], x, y, z)


def get_3d_long_l(obj, hook, x, y, z):
    return smart_instance.get_array_3d_long_l(obj, hook[0], x, y, z)


def get_array_2d_object(obj, hook, x, y):
    return smart_instance.get_array_2d_object(obj, hook[0], x, y)


def get_array_2d_int(obj, hook, x, y):
    return smart_instance.smart.exp_getFieldArray2DInt(smart_instance.target, obj, string_to_char_p(hook[0]), x, y)


def get_array_2d_double(obj, hook, x, y):
    return smart_instance.smart.exp_getFieldArray2DDouble(smart_instance.target, obj, string_to_char_p(hook[0]), x, y)


def get_array_2d_float(obj, hook, x, y):
    return smart_instance.smart.exp_getFieldArray2DFloat(smart_instance.target, obj, string_to_char_p(hook[0]), x, y)


def get_array_2d_bool(obj, hook, x, y):
    return smart_instance.smart.exp_getFieldArray2DBool(smart_instance.target, obj, string_to_char_p(hook[0]), x, y)


def get_array_2d_long_h(obj, hook, x, y):
    return smart_instance.smart.exp_getFieldArray2DLongH(smart_instance.target, obj, hook[0], x, y)


def get_array_2d_long_l(obj, hook, x, y):
    return smart_instance.smart.exp_getFieldArray2DLongL(smart_instance.target, obj, hook[0], x, y)


def get_array_2d_byte(obj, hook, x, y):
    return smart_instance.smart.exp_getFieldArray2DByte(smart_instance.target, obj, hook[0], x, y)


def get_array_2d_char(obj, hook, x, y):
    return smart_instance.smart.exp_getFieldArray2DChar(smart_instance.target, obj, hook[0], x, y)


def get_array_2d_short(obj, hook, x, y):
    return smart_instance.smart.exp_getFieldArray2DShort(smart_instance.target, obj, hook[0], x, y)


def get_array_size(obj, hook, dimension):
    return smart_instance.smart.exp_getFieldArraySize(smart_instance.target, obj, hook[0], dimension)


def get_object_array(obj, hook, index):
    return smart_instance.get_field_array_object(smart_instance.target, obj, hook[0], index)


def get_int_array(obj, hook, index):
    return smart_instance.get_field_array_int(smart_instance.target, obj, hook[0], index)


def get_array_float(obj, hook, index):
    return smart_instance.smart.exp_getFieldArrayFloat(smart_instance.target, obj, hook[0], index)


def get_array_double(obj, hook, index):
    return smart_instance.smart.exp_getFieldArrayDouble(smart_instance.target, obj, hook[0], index)


def get_array_bool(obj, hook, index):
    return smart_instance.smart.exp_getFieldArrayBool(smart_instance.target, obj, hook[0], index)


def get_array_long_h(obj, hook, index):
    return smart_instance.smart.exp_getFieldArrayLongH(smart_instance.target, obj, hook[0], index)


def get_array_long_l(obj, hook, index):
    return smart_instance.smart.exp_getFieldArrayLongL(smart_instance.target, obj, hook[0], index)


def get_array_byte(obj, hook, index):
    return smart_instance.smart.exp_getFieldArrayByte(smart_instance.target, obj, hook[0], index)


def get_array_short(obj, hook, index):
    return smart_instance.smart.exp_getFieldArrayShort(smart_instance.target, obj, hook[0], index)


def get_array_char(obj, hook, index):
    return smart_instance.smart.exp_getFieldArrayChar(smart_instance.target, obj, hook[0], index)


def free_object(obj):
    smart_instance.smart.exp_freeObject(smart_instance.target, obj)


def string_from_string(obj, strng):
    return smart_instance.smart.exp_stringFromString(smart_instance.target, obj, string_to_char_p(strng))


def string_from_chars(obj, strng):
    return smart_instance.smart.exp_stringFromChars(smart_instance.target, obj, string_to_char_p(strng))


def string_from_bytes(obj, strng):
    return smart_instance.smart.exp_stringFromBytes(smart_instance.target, obj, string_to_char_p(strng))


def get_string(obj, hook):
    with get_object(obj, hook) as str_int:
        temp = string_from_string(str_int, 512)
        temp = temp.replace('Â', '')
        temp = temp.replace('#160', '#32')
        return temp


def is_null(obj):
    return smart_instance.smart.exp_isNull(smart_instance.target, obj)


def is_equal(obj):
    return smart_instance.smart.exp_isEqual(smart_instance.target, obj)

