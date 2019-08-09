import ctypes
from _ctypes import POINTER
from ctypes import wintypes, windll

from win32.structs.devmode import DEVMODE
from win32.structs.display_device import DISPLAY_DEVICE
from win32.structs.monitorinfo import MONITORINFOEX, MONITORINFO

# EnumDisplayDevices
_prototype = ctypes.WINFUNCTYPE(wintypes.BOOL,
                                wintypes.LPCWSTR, wintypes.DWORD, POINTER(DISPLAY_DEVICE), wintypes.DWORD)
EnumDisplayDevicesW = _prototype(("EnumDisplayDevicesW", windll.user32))
"""
BOOL EnumDisplayDevicesW(
  LPCWSTR          lpDevice,
  DWORD            iDevNum,
  PDISPLAY_DEVICEW lpDisplayDevice,
  DWORD            dwFlags
);
"""

# EnumDisplaySettings

_prototype = ctypes.WINFUNCTYPE(wintypes.BOOL,
                                wintypes.LPCWSTR, wintypes.DWORD, POINTER(DEVMODE))
EnumDisplaySettingsW = _prototype(("EnumDisplaySettingsW", windll.user32))
"""
BOOL EnumDisplaySettingsW(
  LPCWSTR  lpszDeviceName,
  DWORD    iModeNum,
  DEVMODEW *lpDevMode
);
"""

# GetCursorPos

_prototype = ctypes.WINFUNCTYPE(wintypes.BOOL,
                                wintypes.LPPOINT)
GetCursorPos = _prototype(("GetCursorPos", windll.user32))
"""
BOOL GetCursorPos(
  LPPOINT lpPoint
);
"""

# EnumDisplayMonitors

MonitorEnumProc = ctypes.WINFUNCTYPE(wintypes.BOOL,
                                     wintypes.HMONITOR, wintypes.HDC, wintypes.LPRECT, wintypes.LPARAM)

"""
BOOL EnumDisplayMonitors(
  HDC             hdc,
  LPCRECT         lprcClip,
  MONITORENUMPROC lpfnEnum,
  LPARAM          dwData
);
"""
_prototype = ctypes.WINFUNCTYPE(wintypes.BOOL,
                                wintypes.HDC, wintypes.LPRECT, MonitorEnumProc, wintypes.LPARAM)
EnumDisplayMonitors = _prototype(("EnumDisplayMonitors", windll.user32))
"""
MONITORENUMPROC Monitorenumproc;

BOOL Monitorenumproc(
  HMONITOR Arg1,
  HDC Arg2,
  LPRECT Arg3,
  LPARAM Arg4
)
{...}
"""

# GetMonitorInfo
_prototype = ctypes.WINFUNCTYPE(wintypes.BOOL,
                                wintypes.HMONITOR, POINTER(MONITORINFO))
GetMonitorInfoW = _prototype(("GetMonitorInfoW", windll.user32))
_prototype = ctypes.WINFUNCTYPE(wintypes.BOOL,
                                wintypes.HMONITOR, POINTER(MONITORINFOEX))
GetMonitorInfoExW = _prototype(("GetMonitorInfoW", windll.user32))
"""
BOOL GetMonitorInfoW(
  HMONITOR      hMonitor,
  LPMONITORINFO lpmi
);
"""

# GetSystemMetrics
_prototype = ctypes.WINFUNCTYPE(wintypes.INT,
                                wintypes.INT)
GetSystemMetrics = _prototype(("GetSystemMetrics", windll.user32))
"""
int GetSystemMetrics(
  int nIndex
);
"""
