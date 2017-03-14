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
import Misc.SmartHelpers as Sh
import platform
import ctypes as ct


class Smart:
    def __init__(self):
        if platform.system() == 'Windows':
            self.smart = ct.CDLL('Plugins/libsmartremote64.dll')
        elif platform.system() == 'Darwin':
            self.smart = ct.CDLL('Plugins/libsmartremote32.dylib')
        else:
            self.smart = ct.CDLL('Plugins/libsmartremote32.so')
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
        self.smart.EIOS_RequestTarget.argtypes = [ct.c_char_p]
        self.smart.EIOS_RequestTarget.restype = ct.POINTER(Sh.SMARTClient)
        return self.smart.EIOS_RequestTarget(init_str)

    def release_target(self, target):
        self.smart.EIOS_ReleaseTarget.argtypes = [ct.POINTER(Sh.SMARTClient)]
        self.smart.EIOS_ReleaseTarget.restype = None
        self.smart.EIOS_ReleaseTarget(target)

    def get_target_dimensions(self, target):
        width = ct.c_int()
        height = ct.c_int()
        self.smart.EIOS_GetTargetDimensions.argtypes = [ct.POINTER(ct.c_int), ct.POINTER(ct.c_int)]
        self.smart.EIOS_GetTargetDimensions.restype = None
        self.smart.EIOS_GetTargetDimensions(target, ct.byref(width), ct.byref(height))
        return Sh.Size(width, height)

    def get_image_buffer(self, target):
        self.smart.EIOS_GetImageBuffer.argtypes = [ct.POINTER(Sh.SMARTClient)]
        self.smart.EIOS_GetImageBuffer.restype = ct.POINTER(Sh.RGB)
        return self.smart.EIOS_GetImageBuffer(target)

    def update_image_buffer(self, target):
        self.smart.EIOS_UpdateImageBuffer.argtypes = [ct.POINTER(Sh.SMARTClient)]
        self.smart.EIOS_UpdateImageBuffer.restype = None
        self.smart.EIOS_UpdateImageBuffer(target)

    def get__mouse_position(self, target):
        x = ct.c_int()
        y = ct.c_int()
        self.smart.EIOS_GetMousePosition.argtypes = [
            ct.POINTER(Sh.SMARTClient), ct.POINTER(ct.c_int), ct.POINTER(ct.c_int)]
        self.smart.EIOS_GetMousePosition.restype = None
        self.smart.EIOS_GetMousePosition(target, ct.byref(x), ct.byref(y))
        return Sh.Point(x, y)

    def move_mouse(self, target, x, y):
        self.smart.EIOS_MoveMouse.argtypes = [ct.POINTER(Sh.SMARTClient), ct.c_int, ct.c_int]
        self.smart.EIOS_MoveMouse.restype = None
        self.smart.EIOS_MoveMouse(target, x, y)

    def hold_mouse(self, target, x, y, button):
        self.smart.EIOS_HoldMouse.argtypes = [ct.POINTER(Sh.SMARTClient), ct.c_int, ct.c_int]
        self.smart.EIOS_HoldMouse.restype = None
        self.smart.EIOS_HoldMouse(target, x, y, button)

    def release_mouse(self, target, x, y, button):
        self.smart.EIOS_ReleaseMouse.argtypes = [ct.POINTER(Sh.SMARTClient), ct.c_int, ct.c_int]
        self.smart.EIOS_ReleaseMouse.restype = None
        self.smart.EIOS_ReleaseMouse(target, x, y, button)

    def is_mouse_held(self, target, button):
        self.smart.EIOS_IsMouseHeld.argtypes = [ct.POINTER(Sh.SMARTClient), ct.c_int]
        self.smart.EIOS_IsMouseHeld.restype = ct.c_bool
        return self.smart.EIOS_IsMouseHeld(target, button)

    def scroll_mouse(self, target, x, y, lines):
        self.smart.EIOS_ScrollMouse.argtypes = [ct.POINTER(Sh.SMARTClient), ct.c_int, ct.c_int, ct.c_int]
        self.smart.EIOS_ScrollMouse.restype = None
        self.smart.EIOS_ScrollMouse(target, x, y, lines)

    def send_string(self, target, strng, keywait, keymodwait):
        self.smart.EIOS_SendString.argtypes = [ct.POINTER(Sh.SMARTClient), ct.c_char_p, ct.c_int, ct.c_int]
        self.smart.EIOS_SendString.restype = None
        self.smart.EIOS_SendString(target, strng, keywait, keymodwait)

    def hold_key(self, target, key):
        self.smart.EIOS_HoldKey.argtypes = [ct.POINTER(Sh.SMARTClient), ct.c_int]
        self.smart.EIOS_HoldKey.restype = None
        self.smart.EIOS_HoldKey(target, key)

    def release_key(self, target, key):
        self.smart.EIOS_ReleaseKey.argtypes = [ct.POINTER(Sh.SMARTClient), ct.c_int]
        self.smart.EIOS_ReleaseKey.restype = None
        self.smart.EIOS_ReleaseKey(target, key)

    def is_key_held(self, target, key):
        self.smart.EIOS_IsKeyHeld.argtypes = [ct.POINTER(Sh.SMARTClient), ct.c_int]
        self.smart.EIOS_IsKeyHeld.restype = ct.c_bool
        return self.smart.EIOS_IsKeyHeld(target, key)

    #  PAIRING
    def get_clients(self, only_unpaired):
        self.smart.exp_getClients.argtypes = [ct.c_bool]
        self.smart.exp_getClients.restype = ct.c_int
        return self.smart.exp_getClients(only_unpaired)

    def get_available_pid(self, idx):
        self.smart.exp_getAvailablePID.argtypes = [ct.c_int]
        self.smart.exp_getAvailablePID.restype = ct.c_int
        return self.smart.exp_getAvailablePID(idx)

    def kill_client(self, pid):
        self.smart.exp_killClient.argtypes = [ct.c_int]
        self.smart.exp_killClient.restype = ct.c_bool
        return self.smart.exp_killClient(pid)

    def spawn_client(self, java_exec, remote_path, root, params, width, height, initseq, useragent, javaargs, plugins):
        self.smart.exp_spawnClient.argtypes = [
            ct.c_char_p, ct.c_char_p, ct.c_char_p, ct.c_char_p, ct.c_int, ct.c_int, ct.c_char_p, ct.c_char_p,
            ct.c_char_p, ct.c_char_p]
        self.smart.exp_spawnClient.restype = ct.POINTER(Sh.SMARTClient)
        return self.smart.exp_spawnClient(Sh.string_to_char_p(java_exec), Sh.string_to_char_p(remote_path),
                                          Sh.string_to_char_p(root), Sh.string_to_char_p(params), width, height,
                                          Sh.string_to_char_p(initseq), Sh.string_to_char_p(useragent),
                                          Sh.string_to_char_p(javaargs), Sh.string_to_char_p(plugins))

    def pair_client(self, pid):
        self.smart.exp_pairClient.argtypes = [ct.c_int]
        self.smart.exp_pairClient.restype = ct.POINTER(Sh.SMARTClient)
        return self.smart.exp_pairClient(pid)

    def get_client_pid(self, target):
        self.smart.exp_getClientPID.argtypes = [ct.POINTER(Sh.SMARTClient)]
        self.smart.exp_getClientPID.restype = ct.c_int
        return self.smart.exp_getClientPID(target)

    def free_client(self, target):
        self.smart.exp_freeClient.argtypes = [ct.POINTER(Sh.SMARTClient)]
        self.smart.exp_freeClient.restype = None
        self.smart.exp_freeClient(target)

    def get_image_array_(self, target):
        self.smart.exp_getImageArray.argtypes = [ct.POINTER(Sh.SMARTClient)]
        self.smart.exp_getImageArray.restype = ct.c_void_p
        return self.smart.exp_getImageArray(target)

    def get_debug_array_(self, target):
        self.smart.exp_getDebugArray.argtypes = [ct.POINTER(Sh.SMARTClient)]
        self.smart.exp_getDebugArray.restype = ct.c_void_p
        return self.smart.exp_getDebugArray(target)

    def get_refresh(self, target):
        self.smart.exp_getRefresh.argtypes = [ct.POINTER(Sh.SMARTClient)]
        self.smart.exp_getRefresh.restype = ct.c_int
        return self.smart.exp_getRefresh(target)

    def set_refresh(self, target, value):
        self.smart.exp_setRefresh.argtypes = [ct.POINTER(Sh.SMARTClient), ct.c_int]
        self.smart.exp_setRefresh.restype = None
        self.smart.exp_setRefresh(target, value)

    def set_transparent_color(self, target, colour):
        self.smart.exp_setTransparentColor.argtypes = [ct.POINTER(Sh.SMARTClient), ct.c_int]
        self.smart.exp_setTransparentColor.restype = None
        self.smart.exp_setTransparentColor(target, colour)

    def set_debug(self, target, enabled):
        self.smart.exp_setDebug.argtypes = [ct.POINTER(Sh.SMARTClient), ct.c_bool]
        self.smart.exp_setDebug.restype = None
        self.smart.exp_setDebug(target, enabled)

    def set_graphics(self, target, enabled):
        self.smart.exp_setGraphics.argtypes = [ct.POINTER(Sh.SMARTClient), ct.c_bool]
        self.smart.exp_setGraphics.restype = None
        self.smart.exp_setGraphics(target, enabled)

    def set_enabled(self, target, enabled):
        self.smart.exp_setEnabled.argtypes = [ct.POINTER(Sh.SMARTClient), ct.c_bool]
        self.smart.exp_setEnabled.restype = None
        self.smart.exp_setEnabled(target, enabled)

    def is_active(self, target):
        self.smart.exp_isActive.argtypes = [ct.POINTER(Sh.SMARTClient)]
        self.smart.exp_isActive.restype = ct.c_bool
        return self.smart.exp_isActive(target)

    def is_blocking(self, target):
        self.smart.exp_isBlocking.argtypes = [ct.POINTER(Sh.SMARTClient)]
        self.smart.exp_isBlocking.restype = ct.c_bool
        return self.smart.exp_isBlocking(target)

    def get_mouse_pos(self, target):
        x = ct.c_int()
        y = ct.c_int()
        self.smart.exp_getMousePos.argtypes = [ct.POINTER(Sh.SMARTClient), ct.POINTER(ct.c_int), ct.POINTER(ct.c_int)]
        self.smart.exp_getMousePos.restype = None
        self.smart.exp_getMousePos(target, ct.byref(x), ct.byref(y))
        return Sh.Point(x, y)

    def hold_mouse_(self, target, x, y, left):
        self.smart.exp_holdMouse.argtypes = [ct.POINTER(Sh.SMARTClient), ct.c_int, ct.c_int, ct.c_bool]
        self.smart.exp_holdMouse.restype = None
        self.smart.exp_holdMouse(target, x, y, left)

    def release_mouse_(self, target, x, y, left):
        self.smart.exp_releaseMouse.argtypes = [ct.POINTER(Sh.SMARTClient), ct.c_int, ct.c_int, ct.c_bool]
        self.smart.exp_releaseMouse.restype = None
        self.smart.exp_releaseMouse(target, x, y, left)

    def hold_mouse_plus(self, target, x, y, button):
        self.smart.exp_holdMousePlus.argtypes = [ct.POINTER(Sh.SMARTClient), ct.c_int, ct.c_int, ct.c_int]
        self.smart.exp_holdMousePlus.restype = None
        self.smart.exp_holdMousePlus(target, x, y, button)

    def move_mouse_(self, target, x, y):
        self.smart.exp_moveMouse.argtypes = [ct.POINTER(Sh.SMARTClient), ct.c_int, ct.c_int]
        self.smart.exp_moveMouse.restype = None
        self.smart.exp_moveMouse(target, x, y)

    def wind_mouse_(self, target, x, y):
        self.smart.exp_windMouse.argtypes = [ct.POINTER(Sh.SMARTClient), ct.c_int, ct.c_int]
        self.smart.exp_windMouse.restype = None
        self.smart.exp_windMouse(target, x, y)

    def click_mouse_(self, target, x, y, left):
        self.smart.exp_clickMouse.argtypes = [ct.POINTER(Sh.SMARTClient), ct.c_int, ct.c_int, ct.c_bool]
        self.smart.exp_clickMouse.restype = None
        self.smart.exp_clickMouse(target, x, y, left)

    def click__mouse__plus(self, target, x, y, button):
        self.smart.exp_clickMousePlus.argtypes = [ct.POINTER(Sh.SMARTClient), ct.c_int, ct.c_int, ct.c_int]
        self.smart.exp_clickMousePlus.restype = None
        self.smart.exp_click_mouse_Plus(target, x, y, button)

    def is_mouse_button_held(self, target, button):
        self.smart.exp_isMouseButtonHeld.argtypes = [ct.POINTER(Sh.SMARTClient), ct.c_int]
        self.smart.exp_isMouseButtonHeld.restype = ct.c_bool
        return self.smart.exp_isMouseButtonHeld(target, button)

    def scroll__mouse__(self, target, x, y, lines):
        self.smart.exp_scrollMouse.argtypes = [ct.POINTER(Sh.SMARTClient), ct.c_int, ct.c_int, ct.c_int]
        self.smart.exp_scrollMouse.restype = None
        self.smart.exp_scrollMouse(target, x, y, lines)

    def send_keys(self, target, text, keywait, keymodwait):
        self.smart.exp_sendKeys.argtypes = [ct.POINTER(Sh.SMARTClient), ct.c_char_p, ct.c_int, ct.c_int]
        self.smart.exp_sendKeys.restype = None
        self.smart.exp_sendKeys(target, Sh.string_to_char_p(text), keywait, keymodwait)

    def hold_key_(self, target, code):
        self.smart.exp_holdKey.argtypes = [ct.POINTER(Sh.SMARTClient), ct.c_int]
        self.smart.exp_holdKey.restype = None
        self.smart.exp_holdKey(target, code)

    def release_key_(self, target, code):
        self.smart.exp_releaseKey.argtypes = [ct.POINTER(Sh.SMARTClient), ct.c_int]
        self.smart.exp_releaseKey.restype = None
        self.smart.exp_releaseKey(target, code)

    def is_key_down(self, target, code):
        self.smart.exp_isKeyDown.argtypes = [ct.POINTER(Sh.SMARTClient), ct.c_int]
        self.smart.exp_isKeyDown.restype = ct.c_bool
        return self.smart.exp_isKeyDown(target, code)

    def set_capture(self, target, enabled):
        self.smart.exp_setCapture.argtypes = [ct.POINTER(Sh.SMARTClient), ct.c_bool]
        self.smart.exp_setCapture.restype = None
        self.smart.exp_setCapture(target, enabled)

    def set_native_btn(self, target, pluginid, btnid, state):
        self.smart.exp_setNativeBtn.argtypes = [ct.POINTER(Sh.SMARTClient), ct.c_int, ct.c_int, ct.c_bool]
        self.smart.exp_setNativeBtn.restype = None
        self.smart.exp_setNativeBtn(target, pluginid, btnid, state)

    def get_manifest_hash(self, target):
        self.smart.exp_getManifestHash.argtypes = [ct.POINTER(Sh.SMARTClient)]
        self.smart.exp_getManifestHash.restype = ct.c_int
        return self.smart.exp_getManifestHash(target)

    #  REFLECTION
    def get_field_object(self, target, obj, path):
        self.smart.exp_getFieldObject.argtypes = [ct.POINTER(Sh.SMARTClient), ct.c_void_p, ct.c_char_p]
        self.smart.exp_getFieldObject.restype = ct.c_void_p
        return self.smart.exp_getFieldObject(target, obj, Sh.string_to_char_p(path))

    def is_path_valid(self, target, obj, path):
        self.smart.exp_isPathValid.argtypes = [ct.POINTER(Sh.SMARTClient), ct.c_void_p, ct.c_char_p]
        self.smart.exp_isPathValid.restype = ct.c_bool
        return self.smart.exp_isPathValid(target, obj, Sh.string_to_char_p(path))

    def get_field_boolean(self, target, obj, path):
        self.smart.exp_getFieldBoolean.argtypes = [ct.POINTER(Sh.SMARTClient), ct.c_void_p, ct.c_char_p]
        self.smart.exp_getFieldBoolean.restype = ct.c_bool
        return self.smart.exp_getFieldBoolean(target, obj, Sh.string_to_char_p(path))

    def get_field_long_h(self, target, obj, path):
        self.smart.exp_getFieldLongH.argtypes = [ct.POINTER(Sh.SMARTClient), ct.c_void_p, ct.c_char_p]
        self.smart.exp_getFieldLongH.restype = ct.c_uint
        return self.smart.exp_getFieldLongH(target, obj, Sh.string_to_char_p(path))

    def get_field_long_l(self, target, obj, path):
        self.smart.exp_getFieldLongL.argtypes = [ct.POINTER(Sh.SMARTClient), ct.c_void_p, ct.c_char_p]
        self.smart.exp_getFieldLongL.restype = ct.c_uint
        return self.smart.exp_getFieldLongL(target, obj, Sh.string_to_char_p(path))

    def get_field_int(self, target, obj, path):
        self.smart.exp_getFieldInt.argtypes = [ct.POINTER(Sh.SMARTClient), ct.c_void_p, ct.c_char_p]
        self.smart.exp_getFieldInt.restype = ct.c_int
        return self.smart.exp_getFieldInt(target, obj, Sh.string_to_char_p(path))

    def get_field_short(self, target, obj, path):
        self.smart.exp_getFieldShort.argtypes = [ct.POINTER(Sh.SMARTClient), ct.c_void_p, ct.c_char_p]
        self.smart.exp_getFieldShort.restype = ct.c_int
        return self.smart.exp_getFieldShort(target, obj, Sh.string_to_char_p(path))

    def get_field_float(self, target, obj, path):
        self.smart.exp_getFieldFloat.argtypes = [ct.POINTER(Sh.SMARTClient), ct.c_void_p, ct.c_char_p]
        self.smart.exp_getFieldFloat.restype = ct.c_double
        return self.smart.exp_getFieldFloat(target, obj, Sh.string_to_char_p(path))

    def get_field_double(self, target, obj, path):
        self.smart.exp_getFieldDouble.argtypes = [ct.POINTER(Sh.SMARTClient), ct.c_void_p, ct.c_char_p]
        self.smart.exp_getFieldDouble.restype = ct.c_double
        return self.smart.exp_getFieldDouble(target, obj, Sh.string_to_char_p(path))

    def get_field_byte(self, target, obj, path):
        self.smart.exp_getFieldByte.argtypes = [ct.POINTER(Sh.SMARTClient), ct.c_void_p, ct.c_char_p]
        self.smart.exp_getFieldByte.restype = ct.c_int
        return self.smart.exp_getFieldByte(target, obj, Sh.string_to_char_p(path))

    def get_field_array_3d_object(self, target, obj, path, x, y, z):
        self.smart.exp_getFieldArray3DObject.argtypes = [
            ct.POINTER(Sh.SMARTClient), ct.c_void_p, ct.c_void_p, ct.c_int, ct.c_int, ct.c_int]
        self.smart.exp_getFieldArray3DObject.restype = ct.c_void_p
        return self.smart.exp_getFieldArray3DObject(target, obj, Sh.string_to_char_p(path), x, y, z)

    def get_field_array_3d_char(self, target, obj, path, x, y, z):
        self.smart.exp_getFieldArray3DChar.argtypes = [
            ct.POINTER(Sh.SMARTClient), ct.c_void_p, ct.c_void_p, ct.c_int, ct.c_int, ct.c_int]
        self.smart.exp_getFieldArray3DChar.restype = ct.c_int
        return self.smart.exp_getFieldArray3DChar(target, obj, Sh.string_to_char_p(path), x, y, z)

    def get_field_array_3d_short(self, target, obj, path, x, y, z):
        self.smart.exp_getFieldArray3DShort.argtypes = [
            ct.POINTER(Sh.SMARTClient), ct.c_void_p, ct.c_void_p, ct.c_int, ct.c_int, ct.c_int]
        self.smart.exp_getFieldArray3DShort.restype = ct.c_int
        return self.smart.exp_getFieldArray3DShort(target, obj, Sh.string_to_char_p(path), x, y, z)

    def get_field_array_3d_int(self, target, obj, path, x, y, z):
        self.smart.exp_getFieldArray3DInt.argtypes = [
            ct.POINTER(Sh.SMARTClient), ct.c_void_p, ct.c_void_p, ct.c_int, ct.c_int, ct.c_int]
        self.smart.exp_getFieldArray3DInt.restype = ct.c_int
        return self.smart.exp_getFieldArray3DInt(target, obj, Sh.string_to_char_p(path), x, y, z)

    def get_field_array_3d_float(self, target, obj, path, x, y, z):
        self.smart.exp_getFieldArray3DFloat.argtypes = [
            ct.POINTER(Sh.SMARTClient), ct.c_void_p, ct.c_void_p, ct.c_int, ct.c_int, ct.c_int]
        self.smart.exp_getFieldArray3DFloat.restype = ct.c_float
        return self.smart.exp_getFieldArray3DFloat(target, obj, Sh.string_to_char_p(path), x, y, z)

    def get_field_array_3d_double(self, target, obj, path, x, y, z):
        self.smart.exp_getFieldArray3DDouble.argtypes = [
            ct.POINTER(Sh.SMARTClient), ct.c_void_p, ct.c_void_p, ct.c_int, ct.c_int, ct.c_int]
        self.smart.exp_getFieldArray3DDouble.restype = ct.c_float
        return self.smart.exp_getFieldArray3DDouble(target, obj, Sh.string_to_char_p(path), x, y, z)

    def get_field_array_3d_bool(self, target, obj, path, x, y, z):
        self.smart.exp_getFieldArray3DBool.argtypes = [
            ct.POINTER(Sh.SMARTClient), ct.c_void_p, ct.c_void_p, ct.c_int, ct.c_int, ct.c_int]
        self.smart.exp_getFieldArray3DBool.restype = ct.c_bool
        return self.smart.exp_getFieldArray3DBool(target, obj, Sh.string_to_char_p(path), x, y, z)

    def get_field_array_3d_long_h(self, target, obj, path, x, y, z):
        self.smart.exp_getFieldArray3DLongH.argtypes = [
            ct.POINTER(Sh.SMARTClient), ct.c_void_p, ct.c_void_p, ct.c_int, ct.c_int, ct.c_int]
        self.smart.exp_getFieldArray3DLongH.restype = ct.c_int
        return self.smart.exp_getFieldArray3DLongH(target, obj, Sh.string_to_char_p(path), x, y, z)

    def get_field_array_3d_long_l(self, target, obj, path, x, y, z):
        self.smart.exp_getFieldArray3DLongL.argtypes = [
            ct.POINTER(Sh.SMARTClient), ct.c_void_p, ct.c_void_p, ct.c_int, ct.c_int, ct.c_int]
        self.smart.exp_getFieldArray3DLongL.restype = ct.c_int
        return self.smart.exp_getFieldArray3DLongL(target, obj, Sh.string_to_char_p(path), x, y, z)

    def get_field_array_2d_object(self, target, obj, path, x, y):
        self.smart.exp_getFieldArray2DObject.argtypes = [
            ct.POINTER(Sh.SMARTClient), ct.c_void_p, ct.c_void_p, ct.c_int, ct.c_int]
        self.smart.exp_getFieldArray2DObject.restype = ct.c_void_p
        return self.smart.exp_getFieldArray2DObject(target, obj, Sh.string_to_char_p(path), x, y)

    def get_field_array_2d_int(self, target, obj, path, x, y):
        self.smart.exp_getFieldArray2DInt.argtypes = [
            ct.POINTER(Sh.SMARTClient), ct.c_void_p, ct.c_void_p, ct.c_int, ct.c_int]
        self.smart.exp_getFieldArray2DInt.restype = ct.c_int
        return self.smart.exp_getFieldArray2DInt(target, obj, Sh.string_to_char_p(path), x, y)

    def get_field_array_2d_double(self, target, obj, path, x, y):
        self.smart.exp_getFieldArray2DDouble.argtypes = [
            ct.POINTER(Sh.SMARTClient), ct.c_void_p, ct.c_void_p, ct.c_int, ct.c_int]
        self.smart.exp_getFieldArray2DDouble.restype = ct.c_float
        return self.smart.exp_getFieldArray2DDouble(target, obj, Sh.string_to_char_p(path), x, y)

    def get_field_array_2d_float(self, target, obj, path, x, y):
        self.smart.exp_getFieldArray2DFloat.argtypes = [
            ct.POINTER(Sh.SMARTClient), ct.c_void_p, ct.c_void_p, ct.c_int, ct.c_int]
        self.smart.exp_getFieldArray2DFloat.restype = ct.c_float
        return self.smart.exp_getFieldArray2DFloat(target, obj, Sh.string_to_char_p(path), x, y)

    def get_field_array_2d_bool(self, target, obj, path, x, y):
        self.smart.exp_getFieldArray2DBool.argtypes = [
            ct.POINTER(Sh.SMARTClient), ct.c_void_p, ct.c_void_p, ct.c_int, ct.c_int]
        self.smart.exp_getFieldArray2DBool.restype = ct.c_bool
        return self.smart.exp_getFieldArray2DBool(target, obj, Sh.string_to_char_p(path), x, y)

    def get_field_array_2d_long_h(self, target, obj, path, x, y):
        self.smart.exp_getFieldArray2DLongH.argtypes = [
            ct.POINTER(Sh.SMARTClient), ct.c_void_p, ct.c_void_p, ct.c_int, ct.c_int]
        self.smart.exp_getFieldArray2DLongH.restype = ct.c_int
        return self.smart.exp_getFieldArray2DLongH(target, obj, Sh.string_to_char_p(path), x, y)

    def get_field_array_2d_long_l(self, target, obj, path, x, y):
        self.smart.exp_getFieldArray2DLongL.argtypes = [
            ct.POINTER(Sh.SMARTClient), ct.c_void_p, ct.c_void_p, ct.c_int, ct.c_int]
        self.smart.exp_getFieldArray2DLongL.restype = ct.c_int
        return self.smart.exp_getFieldArray2DLongL(target, obj, Sh.string_to_char_p(path), x, y)

    def get_field_array_2d_byte(self, target, obj, path, x, y):
        self.smart.exp_getFieldArray2DByte.argtypes = [
            ct.POINTER(Sh.SMARTClient), ct.c_void_p, ct.c_void_p, ct.c_int, ct.c_int]
        self.smart.exp_getFieldArray2DByte.restype = ct.c_int
        return self.smart.exp_getFieldArray2DByte(target, obj, Sh.string_to_char_p(path), x, y)

    def get_field_array_2d_char(self, target, obj, path, x, y):
        self.smart.exp_getFieldArray2DChar.argtypes = [
            ct.POINTER(Sh.SMARTClient), ct.c_void_p, ct.c_void_p, ct.c_int, ct.c_int]
        self.smart.exp_getFieldArray2DChar.restype = ct.c_int
        return self.smart.exp_getFieldArray2DChar(target, obj, Sh.string_to_char_p(path), x, y)

    def get_field_array_2d_short(self, target, obj, path, x, y):
        self.smart.exp_getFieldArray2DShort.argtypes = [
            ct.POINTER(Sh.SMARTClient), ct.c_void_p, ct.c_void_p, ct.c_int, ct.c_int]
        self.smart.exp_getFieldArray2DShort.restype = ct.c_int
        return self.smart.exp_getFieldArray2DShort(target, obj, Sh.string_to_char_p(path), x, y)

    def get_field_array_size(self, target, obj, path, dimension):
        self.smart.exp_getFieldArraySize.argtypes = [ct.POINTER(Sh.SMARTClient), ct.c_void_p, ct.c_void_p, ct.c_int]
        self.smart.exp_getFieldArraySize.restype = ct.c_int
        return self.smart.exp_getFieldArraySize(target, obj, Sh.string_to_char_p(path), dimension)

    def get_field_array_object(self, target, obj, path, index):
        self.smart.exp_getFieldArrayObject.argtypes = [ct.POINTER(Sh.SMARTClient), ct.c_void_p, ct.c_void_p, ct.c_int]
        self.smart.exp_getFieldArrayObject.restype = ct.c_void_p
        return self.smart.exp_getFieldArrayObject(target, obj, Sh.string_to_char_p(path), index)

    def get_field_array_int(self, target, obj, path, index):
        self.smart.exp_getFieldArrayInt.argtypes = [ct.POINTER(Sh.SMARTClient), ct.c_void_p, ct.c_void_p, ct.c_int]
        self.smart.exp_getFieldArrayInt.restype = ct.c_int
        return self.smart.exp_getFieldArrayInt(target, obj, Sh.string_to_char_p(path), index)

    def get_field_array_float(self, target, obj, path, index):
        self.smart.exp_getFieldArrayFloat.argtypes = [ct.POINTER(Sh.SMARTClient), ct.c_void_p, ct.c_void_p, ct.c_int]
        self.smart.exp_getFieldArrayFloat.restype = ct.c_float
        return self.smart.exp_getFieldArrayFloat(target, obj, Sh.string_to_char_p(path), index)

    def get_field_array_double(self, target, obj, path, index):
        self.smart.exp_getFieldArrayDouble.argtypes = [ct.POINTER(Sh.SMARTClient), ct.c_void_p, ct.c_void_p, ct.c_int]
        self.smart.exp_getFieldArrayDouble.restype = ct.c_float
        return self.smart.exp_getFieldArrayDouble(target, obj, Sh.string_to_char_p(path), index)

    def get_field_array_bool(self, target, obj, path, index):
        self.smart.exp_getFieldArrayBool.argtypes = [ct.POINTER(Sh.SMARTClient), ct.c_void_p, ct.c_void_p, ct.c_int]
        self.smart.exp_getFieldArrayBool.restype = ct.c_bool
        return self.smart.exp_getFieldArrayBool(target, obj, Sh.string_to_char_p(path), index)

    def get_field_array_long_h(self, target, obj, path, index):
        self.smart.exp_getFieldArrayLongH.argtypes = [ct.POINTER(Sh.SMARTClient), ct.c_void_p, ct.c_void_p, ct.c_int]
        self.smart.exp_getFieldArrayLongH.restype = ct.c_int
        return self.smart.exp_getFieldArrayLongH(target, obj, Sh.string_to_char_p(path), index)

    def get_field_array_long_l(self, target, obj, path, index):
        self.smart.exp_getFieldArrayLongL.argtypes = [ct.POINTER(Sh.SMARTClient), ct.c_void_p, ct.c_void_p, ct.c_int]
        self.smart.exp_getFieldArrayLongL.restype = ct.c_int
        return self.smart.exp_getFieldArrayLongL(target, obj, Sh.string_to_char_p(path), index)

    def get_field_array_byte(self, target, obj, path, index):
        self.smart.exp_getFieldArrayByte.argtypes = [ct.POINTER(Sh.SMARTClient), ct.c_void_p, ct.c_void_p, ct.c_int]
        self.smart.exp_getFieldArrayByte.restype = ct.c_int
        return self.smart.exp_getFieldArrayByte(target, obj, Sh.string_to_char_p(path), index)

    def get_field_array_short(self, target, obj, path, index):
        self.smart.exp_getFieldArrayShort.argtypes = [ct.POINTER(Sh.SMARTClient), ct.c_void_p, ct.c_void_p, ct.c_int]
        self.smart.exp_getFieldArrayShort.restype = ct.c_int
        return self.smart.exp_getFieldArrayShort(target, obj, Sh.string_to_char_p(path), index)

    def get_field_array_char(self, target, obj, path, index):
        self.smart.exp_getFieldArrayChar.argtypes = [ct.POINTER(Sh.SMARTClient), ct.c_void_p, ct.c_void_p, ct.c_int]
        self.smart.exp_getFieldArrayChar.restype = ct.c_int
        return self.smart.exp_getFieldArrayChar(target, obj, Sh.string_to_char_p(path), index)

    def free_object(self, target, obj):
        self.smart.exp_freeObject.argtypes = [ct.POINTER(Sh.SMARTClient), ct.c_void_p]
        self.smart.exp_freeObject.restype = None
        self.smart.exp_freeObject(target, obj)

    def string_from_string(self, target, obj, strng):
        self.smart.exp_stringFromString.argtypes = [ct.POINTER(Sh.SMARTClient), ct.c_void_p, ct.c_char_p]
        self.smart.exp_stringFromString.restype = ct.c_int
        return self.smart.exp_stringFromString(target, obj, Sh.string_to_char_p(strng))

    def string_from_chars(self, target, obj, strng):
        self.smart.exp_stringFromChars.argtypes = [ct.POINTER(Sh.SMARTClient), ct.c_void_p, ct.c_char_p]
        self.smart.exp_stringFromChars.restype = ct.c_int
        return self.smart.exp_stringFromChars(target, obj, Sh.string_to_char_p(strng))

    def string_from_bytes(self, target, obj, strng):
        self.smart.exp_stringFromBytes.argtypes = [ct.POINTER(Sh.SMARTClient), ct.c_void_p, ct.c_char_p]
        self.smart.exp_stringFromBytes.restype = ct.c_int
        return self.smart.exp_stringFromBytes(target, obj, Sh.string_to_char_p(strng))

    def is_null(self, target, obj):
        self.smart.exp_isNull.argtypes = [ct.POINTER(Sh.SMARTClient), ct.c_void_p]
        self.smart.exp_isNull.restype = ct.c_bool
        return self.smart.exp_isNull(target, obj)

    def is_equal(self, target, obj):
        self.smart.exp_isEqual.argtypes = [ct.POINTER(Sh.SMARTClient), ct.c_void_p]
        self.smart.exp_isEqual.restype = ct.c_bool
        return self.smart.exp_isEqual(target, obj)


smart_instance = Smart()
