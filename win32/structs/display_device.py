import ctypes
import enum
from ctypes import wintypes
from win32.structs._base_type import _Win32BaseStruct


# noinspection PyPep8Naming,SpellCheckingInspection
class DISPLAY_DEVICE_FLAGS(enum.IntFlag):
    DISPLAY_DEVICE_ATTACHED_TO_DESKTOP = 0x00000001
    DISPLAY_DEVICE_MULTI_DRIVER = 0x00000002
    DISPLAY_DEVICE_PRIMARY_DEVICE = 0x00000004
    DISPLAY_DEVICE_MIRRORING_DRIVER = 0x00000008
    DISPLAY_DEVICE_VGA_COMPATIBLE = 0x00000010
    DISPLAY_DEVICE_REMOVABLE = 0x00000020
    DISPLAY_DEVICE_MODESPRUNED = 0x08000000
    DISPLAY_DEVICE_REMOTE = 0x04000000
    DISPLAY_DEVICE_DISCONNECT = 0x02000000


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
