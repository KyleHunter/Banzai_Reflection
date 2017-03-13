"""
*   Smart.py credited to Benland100 with modifications by Brandon T
*
*   Smart.py contains wrappers to call smart.dll/dylib/so
*
*   Wrappers for reflection methods are in Reflection.py
*
*   Nothing should be called from within Smart.py other than within Reflection.py
*
*   Global smart_instance is used throughout library as global smart object
"""

from Misc.Misc import *
import platform


class Smart:
    def __init__(self):
        if platform.system() == 'Windows':
            self.smart = CDLL('Plugins/libsmartremote64.dll')
        elif platform.system() == 'Darwin':
            self.smart = CDLL('Plugins/libsmartremote32.dylib')
        else:
            self.smart = CDLL('Plugins/libsmartremote32.so')
        self.target = 0

    #  EIOS

    def launch(self):
        for i in range(0, self.get_clients(True)):
            self.target = self.pair_client(self.get_available_pid(i))
        if self.target == 0:
            self.target = self.spawn_client('java.exe', '.', 'http://oldschool86.runescape.com/',
                                            'j1', 765, 503, '',
                                            'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:33.0) Gecko/20100101 Firefox/33.0',
                                            '', '')

    def free(self):
        self.free_client(smart_instance.target)

    def request_target(self, init_str):
        self.smart.EIOS_RequestTarget.argtypes = [c_char_p]
        self.smart.EIOS_RequestTarget.restype = POINTER(SMARTClient)
        return self.smart.EIOS_RequestTarget(init_str)

    def release_target(self, target):
        self.smart.EIOS_ReleaseTarget.argtypes = [POINTER(SMARTClient)]
        self.smart.EIOS_ReleaseTarget.restype = None
        self.smart.EIOS_ReleaseTarget(target)

    def get_target_dimensions(self, target):
        width = c_int()
        height = c_int()
        self.smart.EIOS_GetTargetDimensions.argtypes = [POINTER(c_int), POINTER(c_int)]
        self.smart.EIOS_GetTargetDimensions.restype = None
        self.smart.EIOS_GetTargetDimensions(target, byref(width), byref(height))
        return Size(width, height)

    def get_image_buffer(self, target):
        self.smart.EIOS_GetImageBuffer.argtypes = [POINTER(SMARTClient)]
        self.smart.EIOS_GetImageBuffer.restype = POINTER(RGB)
        return self.smart.EIOS_GetImageBuffer(target)

    def update_image_buffer(self, target):
        self.smart.EIOS_UpdateImageBuffer.argtypes = [POINTER(SMARTClient)]
        self.smart.EIOS_UpdateImageBuffer.restype = None
        self.smart.EIOS_UpdateImageBuffer(target)

    def get__mouse_position(self, target):
        x = c_int()
        y = c_int()
        self.smart.EIOS_GetMousePosition.argtypes = [POINTER(SMARTClient), POINTER(c_int), POINTER(c_int)]
        self.smart.EIOS_GetMousePosition.restype = None
        self.smart.EIOS_GetMousePosition(target, byref(x), byref(y))
        return Point(x, y)

    def move_mouse(self, target, x, y):
        self.smart.EIOS_MoveMouse.argtypes = [POINTER(SMARTClient), c_int, c_int]
        self.smart.EIOS_MoveMouse.restype = None
        self.smart.EIOS_MoveMouse(target, x, y)

    def hold_mouse(self, target, x, y, button):
        self.smart.EIOS_HoldMouse.argtypes = [POINTER(SMARTClient), c_int, c_int]
        self.smart.EIOS_HoldMouse.restype = None
        self.smart.EIOS_HoldMouse(target, x, y, button)

    def release_mouse(self, target, x, y, button):
        self.smart.EIOS_ReleaseMouse.argtypes = [POINTER(SMARTClient), c_int, c_int]
        self.smart.EIOS_ReleaseMouse.restype = None
        self.smart.EIOS_ReleaseMouse(target, x, y, button)

    def is_mouse_held(self, target, button):
        self.smart.EIOS_IsMouseHeld.argtypes = [POINTER(SMARTClient), c_int]
        self.smart.EIOS_IsMouseHeld.restype = c_bool
        return self.smart.EIOS_IsMouseHeld(target, button)

    def scroll_mouse(self, target, x, y, lines):
        self.smart.EIOS_ScrollMouse.argtypes = [POINTER(SMARTClient), c_int, c_int, c_int]
        self.smart.EIOS_ScrollMouse.restype = None
        self.smart.EIOS_ScrollMouse(target, x, y, lines)

    def send_string(self, target, strng, keywait, keymodwait):
        self.smart.EIOS_SendString.argtypes = [POINTER(SMARTClient), c_char_p, c_int, c_int]
        self.smart.EIOS_SendString.restype = None
        self.smart.EIOS_SendString(target, strng, keywait, keymodwait)

    def hold_key(self, target, key):
        self.smart.EIOS_HoldKey.argtypes = [POINTER(SMARTClient), c_int]
        self.smart.EIOS_HoldKey.restype = None
        self.smart.EIOS_HoldKey(target, key)

    def release_key(self, target, key):
        self.smart.EIOS_ReleaseKey.argtypes = [POINTER(SMARTClient), c_int]
        self.smart.EIOS_ReleaseKey.restype = None
        self.smart.EIOS_ReleaseKey(target, key)

    def is_key_held(self, target, key):
        self.smart.EIOS_IsKeyHeld.argtypes = [POINTER(SMARTClient), c_int]
        self.smart.EIOS_IsKeyHeld.restype = c_bool
        return self.smart.EIOS_IsKeyHeld(target, key)

    #  PAIRING
    def get_clients(self, only_unpaired):
        self.smart.exp_getClients.argtypes = [c_bool]
        self.smart.exp_getClients.restype = c_int
        return self.smart.exp_getClients(only_unpaired)

    def get_available_pid(self, idx):
        self.smart.exp_getAvailablePID.argtypes = [c_int]
        self.smart.exp_getAvailablePID.restype = c_int
        return self.smart.exp_getAvailablePID(idx)

    def kill_client(self, pid):
        self.smart.exp_killClient.argtypes = [c_int]
        self.smart.exp_killClient.restype = c_bool
        return self.smart.exp_killClient(pid)

    def spawn_client(self, java_exec, remote_path, root, params, width, height, initseq, useragent, javaargs, plugins):
        self.smart.exp_spawnClient.argtypes = [c_char_p, c_char_p, c_char_p, c_char_p, c_int, c_int, c_char_p, c_char_p,
                                               c_char_p, c_char_p]
        self.smart.exp_spawnClient.restype = POINTER(SMARTClient)
        return self.smart.exp_spawnClient(string_to_char_p(java_exec), string_to_char_p(remote_path),
                                          string_to_char_p(root), string_to_char_p(params), width, height,
                                          string_to_char_p(initseq), string_to_char_p(useragent),
                                          string_to_char_p(javaargs), string_to_char_p(plugins))

    def pair_client(self, pid):
        self.smart.exp_pairClient.argtypes = [c_int]
        self.smart.exp_pairClient.restype = POINTER(SMARTClient)
        return self.smart.exp_pairClient(pid)

    def get_client_pid(self, target):
        self.smart.exp_getClientPID.argtypes = [POINTER(SMARTClient)]
        self.smart.exp_getClientPID.restype = c_int
        return self.smart.exp_getClientPID(target)

    def free_client(self, target):
        self.smart.exp_freeClient.argtypes = [POINTER(SMARTClient)]
        self.smart.exp_freeClient.restype = None
        self.smart.exp_freeClient(target)

    def get_image_array_(self, target):
        self.smart.exp_getImageArray.argtypes = [POINTER(SMARTClient)]
        self.smart.exp_getImageArray.restype = c_void_p
        return self.smart.exp_getImageArray(target)

    def get_debug_array_(self, target):
        self.smart.exp_getDebugArray.argtypes = [POINTER(SMARTClient)]
        self.smart.exp_getDebugArray.restype = c_void_p
        return self.smart.exp_getDebugArray(target)

    def get_refresh(self, target):
        self.smart.exp_getRefresh.argtypes = [POINTER(SMARTClient)]
        self.smart.exp_getRefresh.restype = c_int
        return self.smart.exp_getRefresh(target)

    def set_refresh(self, target, value):
        self.smart.exp_setRefresh.argtypes = [POINTER(SMARTClient), c_int]
        self.smart.exp_setRefresh.restype = None
        self.smart.exp_setRefresh(target, value)

    def set_transparent_color(self, target, colour):
        self.smart.exp_setTransparentColor.argtypes = [POINTER(SMARTClient), c_int]
        self.smart.exp_setTransparentColor.restype = None
        self.smart.exp_setTransparentColor(target, colour)

    def set_debug(self, target, enabled):
        self.smart.exp_setDebug.argtypes = [POINTER(SMARTClient), c_bool]
        self.smart.exp_setDebug.restype = None
        self.smart.exp_setDebug(target, enabled)

    def set_graphics(self, target, enabled):
        self.smart.exp_setGraphics.argtypes = [POINTER(SMARTClient), c_bool]
        self.smart.exp_setGraphics.restype = None
        self.smart.exp_setGraphics(target, enabled)

    def set_enabled(self, target, enabled):
        self.smart.exp_setEnabled.argtypes = [POINTER(SMARTClient), c_bool]
        self.smart.exp_setEnabled.restype = None
        self.smart.exp_setEnabled(target, enabled)

    def is_active(self, target):
        self.smart.exp_isActive.argtypes = [POINTER(SMARTClient)]
        self.smart.exp_isActive.restype = c_bool
        return self.smart.exp_isActive(target)

    def is_blocking(self, target):
        self.smart.exp_isBlocking.argtypes = [POINTER(SMARTClient)]
        self.smart.exp_isBlocking.restype = c_bool
        return self.smart.exp_isBlocking(target)

    def get_mouse_pos(self, target):
        x = c_int()
        y = c_int()
        self.smart.exp_getMousePos.argtypes = [POINTER(SMARTClient), POINTER(c_int), POINTER(c_int)]
        self.smart.exp_getMousePos.restype = None
        self.smart.exp_getMousePos(target, byref(x), byref(y))
        return Point(x, y)

    def hold_mouse_(self, target, x, y, left):
        self.smart.exp_holdMouse.argtypes = [POINTER(SMARTClient), c_int, c_int, c_bool]
        self.smart.exp_holdMouse.restype = None
        self.smart.exp_holdMouse(target, x, y, left)

    def release_mouse_(self, target, x, y, left):
        self.smart.exp_releaseMouse.argtypes = [POINTER(SMARTClient), c_int, c_int, c_bool]
        self.smart.exp_releaseMouse.restype = None
        self.smart.exp_releaseMouse(target, x, y, left)

    def hold_mouse_plus(self, target, x, y, button):
        self.smart.exp_holdMousePlus.argtypes = [POINTER(SMARTClient), c_int, c_int, c_int]
        self.smart.exp_holdMousePlus.restype = None
        self.smart.exp_holdMousePlus(target, x, y, button)

    def move_mouse_(self, target, x, y):
        self.smart.exp_moveMouse.argtypes = [POINTER(SMARTClient), c_int, c_int]
        self.smart.exp_moveMouse.restype = None
        self.smart.exp_moveMouse(target, x, y)

    def wind_mouse_(self, target, x, y):
        self.smart.exp_windMouse.argtypes = [POINTER(SMARTClient), c_int, c_int]
        self.smart.exp_windMouse.restype = None
        self.smart.exp_windMouse(target, x, y)

    def click_mouse_(self, target, x, y, left):
        self.smart.exp_clickMouse.argtypes = [POINTER(SMARTClient), c_int, c_int, c_bool]
        self.smart.exp_clickMouse.restype = None
        self.smart.exp_clickMouse(target, x, y, left)

    def click__mouse__plus(self, target, x, y, button):
        self.smart.exp_clickMousePlus.argtypes = [POINTER(SMARTClient), c_int, c_int, c_int]
        self.smart.exp_clickMousePlus.restype = None
        self.smart.exp_click_mouse_Plus(target, x, y, button)

    def is_mouse_button_held(self, target, button):
        self.smart.exp_isMouseButtonHeld.argtypes = [POINTER(SMARTClient), c_int]
        self.smart.exp_isMouseButtonHeld.restype = c_bool
        return self.smart.exp_isMouseButtonHeld(target, button)

    def scroll__mouse__(self, target, x, y, lines):
        self.smart.exp_scrollMouse.argtypes = [POINTER(SMARTClient), c_int, c_int, c_int]
        self.smart.exp_scrollMouse.restype = None
        self.smart.exp_scrollMouse(target, x, y, lines)

    def send_keys(self, target, text, keywait, keymodwait):
        self.smart.exp_sendKeys.argtypes = [POINTER(SMARTClient), c_char_p, c_int, c_int]
        self.smart.exp_sendKeys.restype = None
        self.smart.exp_sendKeys(target, string_to_char_p(text), keywait, keymodwait)

    def hold_key_(self, target, code):
        self.smart.exp_holdKey.argtypes = [POINTER(SMARTClient), c_int]
        self.smart.exp_holdKey.restype = None
        self.smart.exp_holdKey(target, code)

    def release_key_(self, target, code):
        self.smart.exp_releaseKey.argtypes = [POINTER(SMARTClient), c_int]
        self.smart.exp_releaseKey.restype = None
        self.smart.exp_releaseKey(target, code)

    def is_key_down(self, target, code):
        self.smart.exp_isKeyDown.argtypes = [POINTER(SMARTClient), c_int]
        self.smart.exp_isKeyDown.restype = c_bool
        return self.smart.exp_isKeyDown(target, code)

    def set_capture(self, target, enabled):
        self.smart.exp_setCapture.argtypes = [POINTER(SMARTClient), c_bool]
        self.smart.exp_setCapture.restype = None
        self.smart.exp_setCapture(target, enabled)

    def set_native_btn(self, target, pluginid, btnid, state):
        self.smart.exp_setNativeBtn.argtypes = [POINTER(SMARTClient), c_int, c_int, c_bool]
        self.smart.exp_setNativeBtn.restype = None
        self.smart.exp_setNativeBtn(target, pluginid, btnid, state)

    def get_manifest_hash(self, target):
        self.smart.exp_getManifestHash.argtypes = [POINTER(SMARTClient)]
        self.smart.exp_getManifestHash.restype = c_int
        return self.smart.exp_getManifestHash(target)

    #  REFLECTION
    def get_field_object(self, target, obj, path):
        self.smart.exp_getFieldObject.argtypes = [POINTER(SMARTClient), c_void_p, c_char_p]
        self.smart.exp_getFieldObject.restype = c_void_p
        return self.smart.exp_getFieldObject(target, obj, string_to_char_p(path))

    def is_path_valid(self, target, obj, path):
        self.smart.exp_isPathValid.argtypes = [POINTER(SMARTClient), c_void_p, c_char_p]
        self.smart.exp_isPathValid.restype = c_bool
        return self.smart.exp_isPathValid(target, obj, string_to_char_p(path))

    def get_field_boolean(self, target, obj, path):
        self.smart.exp_getFieldBoolean.argtypes = [POINTER(SMARTClient), c_void_p, c_char_p]
        self.smart.exp_getFieldBoolean.restype = c_bool
        return self.smart.exp_getFieldBoolean(target, obj, string_to_char_p(path))

    def get_field_long_h(self, target, obj, path):
        self.smart.exp_getFieldLongH.argtypes = [POINTER(SMARTClient), c_void_p, c_char_p]
        self.smart.exp_getFieldLongH.restype = c_uint
        return self.smart.exp_getFieldLongH(target, obj, string_to_char_p(path))

    def get_field_long_l(self, target, obj, path):
        self.smart.exp_getFieldLongL.argtypes = [POINTER(SMARTClient), c_void_p, c_char_p]
        self.smart.exp_getFieldLongL.restype = c_uint
        return self.smart.exp_getFieldLongL(target, obj, string_to_char_p(path))

    def get_field_int(self, target, obj, path):
        self.smart.exp_getFieldInt.argtypes = [POINTER(SMARTClient), c_void_p, c_char_p]
        self.smart.exp_getFieldInt.restype = c_int
        return self.smart.exp_getFieldInt(target, obj, string_to_char_p(path))

    def get_field_short(self, target, obj, path):
        self.smart.exp_getFieldShort.argtypes = [POINTER(SMARTClient), c_void_p, c_char_p]
        self.smart.exp_getFieldShort.restype = c_int
        return self.smart.exp_getFieldShort(target, obj, string_to_char_p(path))

    def get_field_float(self, target, obj, path):
        self.smart.exp_getFieldFloat.argtypes = [POINTER(SMARTClient), c_void_p, c_char_p]
        self.smart.exp_getFieldFloat.restype = c_double
        return self.smart.exp_getFieldFloat(target, obj, string_to_char_p(path))

    def get_field_double(self, target, obj, path):
        self.smart.exp_getFieldDouble.argtypes = [POINTER(SMARTClient), c_void_p, c_char_p]
        self.smart.exp_getFieldDouble.restype = c_double
        return self.smart.exp_getFieldDouble(target, obj, string_to_char_p(path))

    def get_field_byte(self, target, obj, path):
        self.smart.exp_getFieldByte.argtypes = [POINTER(SMARTClient), c_void_p, c_char_p]
        self.smart.exp_getFieldByte.restype = c_int
        return self.smart.exp_getFieldByte(target, obj, string_to_char_p(path))

    def get_field_array_3d_object(self, target, obj, path, x, y, z):
        self.smart.exp_getFieldArray3DObject.argtypes = [POINTER(SMARTClient), c_void_p, c_void_p, c_int, c_int, c_int]
        self.smart.exp_getFieldArray3DObject.restype = c_void_p
        return self.smart.exp_getFieldArray3DObject(target, obj, string_to_char_p(path), x, y, z)

    def get_field_array_3d_char(self, target, obj, path, x, y, z):
        self.smart.exp_getFieldArray3DChar.argtypes = [POINTER(SMARTClient), c_void_p, c_void_p, c_int, c_int, c_int]
        self.smart.exp_getFieldArray3DChar.restype = c_int
        return self.smart.exp_getFieldArray3DChar(target, obj, string_to_char_p(path), x, y, z)

    def get_field_array_3d_short(self, target, obj, path, x, y, z):
        self.smart.exp_getFieldArray3DShort.argtypes = [POINTER(SMARTClient), c_void_p, c_void_p, c_int, c_int, c_int]
        self.smart.exp_getFieldArray3DShort.restype = c_int
        return self.smart.exp_getFieldArray3DShort(target, obj, string_to_char_p(path), x, y, z)

    def get_field_array_3d_int(self, target, obj, path, x, y, z):
        self.smart.exp_getFieldArray3DInt.argtypes = [POINTER(SMARTClient), c_void_p, c_void_p, c_int, c_int, c_int]
        self.smart.exp_getFieldArray3DInt.restype = c_int
        return self.smart.exp_getFieldArray3DInt(target, obj, string_to_char_p(path), x, y, z)

    def get_field_array_3d_float(self, target, obj, path, x, y, z):
        self.smart.exp_getFieldArray3DFloat.argtypes = [POINTER(SMARTClient), c_void_p, c_void_p, c_int, c_int, c_int]
        self.smart.exp_getFieldArray3DFloat.restype = c_float
        return self.smart.exp_getFieldArray3DFloat(target, obj, string_to_char_p(path), x, y, z)

    def get_field_array_3d_double(self, target, obj, path, x, y, z):
        self.smart.exp_getFieldArray3DDouble.argtypes = [POINTER(SMARTClient), c_void_p, c_void_p, c_int, c_int, c_int]
        self.smart.exp_getFieldArray3DDouble.restype = c_float
        return self.smart.exp_getFieldArray3DDouble(target, obj, string_to_char_p(path), x, y, z)

    def get_field_array_3d_bool(self, target, obj, path, x, y, z):
        self.smart.exp_getFieldArray3DBool.argtypes = [POINTER(SMARTClient), c_void_p, c_void_p, c_int, c_int, c_int]
        self.smart.exp_getFieldArray3DBool.restype = c_bool
        return self.smart.exp_getFieldArray3DBool(target, obj, string_to_char_p(path), x, y, z)

    def get_field_array_3d_long_h(self, target, obj, path, x, y, z):
        self.smart.exp_getFieldArray3DLongH.argtypes = [POINTER(SMARTClient), c_void_p, c_void_p, c_int, c_int, c_int]
        self.smart.exp_getFieldArray3DLongH.restype = c_int
        return self.smart.exp_getFieldArray3DLongH(target, obj, string_to_char_p(path), x, y, z)

    def get_field_array_3d_long_l(self, target, obj, path, x, y, z):
        self.smart.exp_getFieldArray3DLongL.argtypes = [POINTER(SMARTClient), c_void_p, c_void_p, c_int, c_int, c_int]
        self.smart.exp_getFieldArray3DLongL.restype = c_int
        return self.smart.exp_getFieldArray3DLongL(target, obj, string_to_char_p(path), x, y, z)

    def get_field_array_2d_object(self, target, obj, path, x, y):
        self.smart.exp_getFieldArray2DObject.argtypes = [POINTER(SMARTClient), c_void_p, c_void_p, c_int, c_int]
        self.smart.exp_getFieldArray2DObject.restype = c_void_p
        return self.smart.exp_getFieldArray2DObject(target, obj, string_to_char_p(path), x, y)

    def get_field_array_2d_int(self, target, obj, path, x, y):
        self.smart.exp_getFieldArray2DInt.argtypes = [POINTER(SMARTClient), c_void_p, c_void_p, c_int, c_int]
        self.smart.exp_getFieldArray2DInt.restype = c_int
        return self.smart.exp_getFieldArray2DInt(target, obj, string_to_char_p(path), x, y)

    def get_field_array_2d_double(self, target, obj, path, x, y):
        self.smart.exp_getFieldArray2DDouble.argtypes = [POINTER(SMARTClient), c_void_p, c_void_p, c_int, c_int]
        self.smart.exp_getFieldArray2DDouble.restype = c_float
        return self.smart.exp_getFieldArray2DDouble(target, obj, string_to_char_p(path), x, y)

    def get_field_array_2d_float(self, target, obj, path, x, y):
        self.smart.exp_getFieldArray2DFloat.argtypes = [POINTER(SMARTClient), c_void_p, c_void_p, c_int, c_int]
        self.smart.exp_getFieldArray2DFloat.restype = c_float
        return self.smart.exp_getFieldArray2DFloat(target, obj, string_to_char_p(path), x, y)

    def get_field_array_2d_bool(self, target, obj, path, x, y):
        self.smart.exp_getFieldArray2DBool.argtypes = [POINTER(SMARTClient), c_void_p, c_void_p, c_int, c_int]
        self.smart.exp_getFieldArray2DBool.restype = c_bool
        return self.smart.exp_getFieldArray2DBool(target, obj, string_to_char_p(path), x, y)

    def get_field_array_2d_long_h(self, target, obj, path, x, y):
        self.smart.exp_getFieldArray2DLongH.argtypes = [POINTER(SMARTClient), c_void_p, c_void_p, c_int, c_int]
        self.smart.exp_getFieldArray2DLongH.restype = c_int
        return self.smart.exp_getFieldArray2DLongH(target, obj, string_to_char_p(path), x, y)

    def get_field_array_2d_long_l(self, target, obj, path, x, y):
        self.smart.exp_getFieldArray2DLongL.argtypes = [POINTER(SMARTClient), c_void_p, c_void_p, c_int, c_int]
        self.smart.exp_getFieldArray2DLongL.restype = c_int
        return self.smart.exp_getFieldArray2DLongL(target, obj, string_to_char_p(path), x, y)

    def get_field_array_2d_byte(self, target, obj, path, x, y):
        self.smart.exp_getFieldArray2DByte.argtypes = [POINTER(SMARTClient), c_void_p, c_void_p, c_int, c_int]
        self.smart.exp_getFieldArray2DByte.restype = c_int
        return self.smart.exp_getFieldArray2DByte(target, obj, string_to_char_p(path), x, y)

    def get_field_array_2d_char(self, target, obj, path, x, y):
        self.smart.exp_getFieldArray2DChar.argtypes = [POINTER(SMARTClient), c_void_p, c_void_p, c_int, c_int]
        self.smart.exp_getFieldArray2DChar.restype = c_int
        return self.smart.exp_getFieldArray2DChar(target, obj, string_to_char_p(path), x, y)

    def get_field_array_2d_short(self, target, obj, path, x, y):
        self.smart.exp_getFieldArray2DShort.argtypes = [POINTER(SMARTClient), c_void_p, c_void_p, c_int, c_int]
        self.smart.exp_getFieldArray2DShort.restype = c_int
        return self.smart.exp_getFieldArray2DShort(target, obj, string_to_char_p(path), x, y)

    def get_field_array_size(self, target, obj, path, dimension):
        self.smart.exp_getFieldArraySize.argtypes = [POINTER(SMARTClient), c_void_p, c_void_p, c_int]
        self.smart.exp_getFieldArraySize.restype = c_int
        return self.smart.exp_getFieldArraySize(target, obj, string_to_char_p(path), dimension)

    def get_field_array_object(self, target, obj, path, index):
        self.smart.exp_getFieldArrayObject.argtypes = [POINTER(SMARTClient), c_void_p, c_void_p, c_int]
        self.smart.exp_getFieldArrayObject.restype = c_void_p
        return self.smart.exp_getFieldArrayObject(target, obj, string_to_char_p(path), index)

    def get_field_array_int(self, target, obj, path, index):
        self.smart.exp_getFieldArrayInt.argtypes = [POINTER(SMARTClient), c_void_p, c_void_p, c_int]
        self.smart.exp_getFieldArrayInt.restype = c_int
        return self.smart.exp_getFieldArrayInt(target, obj, string_to_char_p(path), index)

    def get_field_array_float(self, target, obj, path, index):
        self.smart.exp_getFieldArrayFloat.argtypes = [POINTER(SMARTClient), c_void_p, c_void_p, c_int]
        self.smart.exp_getFieldArrayFloat.restype = c_float
        return self.smart.exp_getFieldArrayFloat(target, obj, string_to_char_p(path), index)

    def get_field_array_double(self, target, obj, path, index):
        self.smart.exp_getFieldArrayDouble.argtypes = [POINTER(SMARTClient), c_void_p, c_void_p, c_int]
        self.smart.exp_getFieldArrayDouble.restype = c_float
        return self.smart.exp_getFieldArrayDouble(target, obj, string_to_char_p(path), index)

    def get_field_array_bool(self, target, obj, path, index):
        self.smart.exp_getFieldArrayBool.argtypes = [POINTER(SMARTClient), c_void_p, c_void_p, c_int]
        self.smart.exp_getFieldArrayBool.restype = c_bool
        return self.smart.exp_getFieldArrayBool(target, obj, string_to_char_p(path), index)

    def get_field_array_long_h(self, target, obj, path, index):
        self.smart.exp_getFieldArrayLongH.argtypes = [POINTER(SMARTClient), c_void_p, c_void_p, c_int]
        self.smart.exp_getFieldArrayLongH.restype = c_int
        return self.smart.exp_getFieldArrayLongH(target, obj, string_to_char_p(path), index)

    def get_field_array_long_l(self, target, obj, path, index):
        self.smart.exp_getFieldArrayLongL.argtypes = [POINTER(SMARTClient), c_void_p, c_void_p, c_int]
        self.smart.exp_getFieldArrayLongL.restype = c_int
        return self.smart.exp_getFieldArrayLongL(target, obj, string_to_char_p(path), index)

    def get_field_array_byte(self, target, obj, path, index):
        self.smart.exp_getFieldArrayByte.argtypes = [POINTER(SMARTClient), c_void_p, c_void_p, c_int]
        self.smart.exp_getFieldArrayByte.restype = c_int
        return self.smart.exp_getFieldArrayByte(target, obj, string_to_char_p(path), index)

    def get_field_array_short(self, target, obj, path, index):
        self.smart.exp_getFieldArrayShort.argtypes = [POINTER(SMARTClient), c_void_p, c_void_p, c_int]
        self.smart.exp_getFieldArrayShort.restype = c_int
        return self.smart.exp_getFieldArrayShort(target, obj, string_to_char_p(path), index)

    def get_field_array_char(self, target, obj, path, index):
        self.smart.exp_getFieldArrayChar.argtypes = [POINTER(SMARTClient), c_void_p, c_void_p, c_int]
        self.smart.exp_getFieldArrayChar.restype = c_int
        return self.smart.exp_getFieldArrayChar(target, obj, string_to_char_p(path), index)

    def free_object(self, target, obj):
        self.smart.exp_freeObject.argtypes = [POINTER(SMARTClient), c_void_p]
        self.smart.exp_freeObject.restype = None
        self.smart.exp_freeObject(target, obj)

    def string_from_string(self, target, obj, strng):
        self.smart.exp_stringFromString.argtypes = [POINTER(SMARTClient), c_void_p, c_char_p]
        self.smart.exp_stringFromString.restype = c_int
        return self.smart.exp_stringFromString(target, obj, string_to_char_p(strng))

    def string_from_chars(self, target, obj, strng):
        self.smart.exp_stringFromChars.argtypes = [POINTER(SMARTClient), c_void_p, c_char_p]
        self.smart.exp_stringFromChars.restype = c_int
        return self.smart.exp_stringFromChars(target, obj, string_to_char_p(strng))

    def string_from_bytes(self, target, obj, strng):
        self.smart.exp_stringFromBytes.argtypes = [POINTER(SMARTClient), c_void_p, c_char_p]
        self.smart.exp_stringFromBytes.restype = c_int
        return self.smart.exp_stringFromBytes(target, obj, string_to_char_p(strng))

    def is_null(self, target, obj):
        self.smart.exp_isNull.argtypes = [POINTER(SMARTClient), c_void_p]
        self.smart.exp_isNull.restype = c_bool
        return self.smart.exp_isNull(target, obj)

    def is_equal(self, target, obj):
        self.smart.exp_isEqual.argtypes = [POINTER(SMARTClient), c_void_p]
        self.smart.exp_isEqual.restype = c_bool
        return self.smart.exp_isEqual(target, obj)


smart_instance = Smart()
