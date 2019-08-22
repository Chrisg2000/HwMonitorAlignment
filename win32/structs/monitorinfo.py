import ctypes
from ctypes import wintypes

from win32.structs._base_type import _Win32BaseStruct, CCHDEVICENAME


class MONITORINFO(_Win32BaseStruct):
    """
    typedef struct tagMONITORINFO {
    DWORD cbSize;
      RECT  rcMonitor;
      RECT  rcWork;
      DWORD dwFlags;
    } MONITORINFO, *LPMONITORINFO;
    """
    _fields_ = [
        ("cbSize", wintypes.DWORD),
        ("rcMonitor", wintypes.RECT),
        ("rcWork", wintypes.RECT),
        ("dwFlags", wintypes.DWORD),
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cbSize = ctypes.sizeof(MONITORINFO)


class MONITORINFOEX(_Win32BaseStruct):
    """
    typedef struct tagMONITORINFOEX {
      DWORD cbSize;
      RECT  rcMonitor;
      RECT  rcWork;
      DWORD dwFlags;
      TCHAR szDevice[CCHDEVICENAME];
    } MONITORINFOEX, *LPMONITORINFOEX;
    """
    _fields_ = [
        ("cbSize", wintypes.DWORD),
        ("rcMonitor", wintypes.RECT),
        ("rcWork", wintypes.RECT),
        ("dwFlags", wintypes.DWORD),
        ("szDevice", wintypes.WCHAR * CCHDEVICENAME)
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cbSize = ctypes.sizeof(MONITORINFOEX)
