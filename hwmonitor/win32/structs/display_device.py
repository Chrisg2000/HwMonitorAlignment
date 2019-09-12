import ctypes
from ctypes import wintypes

from hwmonitor.win32.structs._base_type import _Win32BaseStruct


# noinspection PyTypeChecker
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
