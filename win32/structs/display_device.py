import ctypes
import enum
from ctypes import wintypes
from win32.structs._base_type import _Win32BaseStruct


class DISPLAY_DEVICE_FLAGS(enum.IntFlag):
    DISPLAY_DEVICE_ACTIVE = 0x1
    DISPLAY_DEVICE_MULTI_DRIVER = 0x2
    DISPLAY_DEVICE_PRIMARY_DEVICE = 0x4
    DISPLAY_DEVICE_MIRRORING_DRIVER = 0x8
    DISPLAY_DEVICE_VGA_COMPATIBLE = 0x10
    DISPLAY_DEVICE_REMOVABLE = 0x20
    DISPLAY_DEVICE_DISCONNECT = 0x2000000
    DISPLAY_DEVICE_REMOTE = 0x4000000
    DISPLAY_DEVICE_MODESPRUNED = 0x8000000


# noinspection PyPep8Naming,PyTypeChecker,SpellCheckingInspection
class DISPLAY_DEVICE(_Win32BaseStruct):
    """https://docs.microsoft.com/en-us/windows/win32/api/wingdi/ns-wingdi-display_devicew
    typedef struct _DISPLAY_DEVICEW {
      DWORD cb;
      WCHAR DeviceName[32];
      WCHAR DeviceString[128];
      DWORD StateFlags;
      WCHAR DeviceID[128];
      WCHAR DeviceKey[128];
    } DISPLAY_DEVICEW, *PDISPLAY_DEVICEW, *LPDISPLAY_DEVICEW;
    """
    _fields_ = [
        ("cb", wintypes.DWORD),
        ("DeviceName", wintypes.WCHAR * 32),
        ("DeviceString", wintypes.WCHAR * 128),
        ("StateFlags", wintypes.DWORD),
        ("DeviceID", wintypes.WCHAR * 128),
        ("DeviceKey", wintypes.WCHAR * 128)
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cb = ctypes.sizeof(DISPLAY_DEVICE)
