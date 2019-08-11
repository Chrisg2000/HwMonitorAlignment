import ctypes
from ctypes import windll, POINTER, byref, wintypes

from win32._util import function_factory, check_zero
from win32.structs.devmode import DEVMODE
from win32.structs.display_device import DISPLAY_DEVICE
from win32.structs.monitorinfo import MONITORINFO, MONITORINFOEX

# EnumDisplayDevices

_BaseEnumDisplayDevices = function_factory(
    windll.user32.EnumDisplayDevicesW,
    [wintypes.LPCWSTR, wintypes.DWORD, POINTER(DISPLAY_DEVICE), wintypes.DWORD],
    wintypes.BOOL,
    check_zero)


def EnumDisplayDevices(lpDevice, iDevNum, dwFlags):
    """
    BOOL EnumDisplayDevicesW(
      LPCWSTR          lpDevice,
      DWORD            iDevNum,
      PDISPLAY_DEVICEW lpDisplayDevice,
      DWORD            dwFlags
    );
    """
    py_DISPLAY_DEVICE = DISPLAY_DEVICE()
    _BaseEnumDisplayDevices(lpDevice, iDevNum, byref(py_DISPLAY_DEVICE), dwFlags)
    return py_DISPLAY_DEVICE


# EnumDisplaySettings

_BaseEnumDisplaySettings = function_factory(
    windll.user32.EnumDisplaySettingsW,
    [wintypes.LPCWSTR, wintypes.DWORD, POINTER(DEVMODE)],
    wintypes.BOOL,
    check_zero
)


def EnumDisplaySettings(lpszDeviceName, iModeNum):
    """
    BOOL EnumDisplaySettingsW(
      LPCWSTR  lpszDeviceName,
      DWORD    iModeNum,
      DEVMODEW *lpDevMode
    );
    """
    py_DEVMODE = DEVMODE()
    _BaseEnumDisplaySettings(lpszDeviceName, iModeNum, byref(py_DEVMODE))
    return py_DEVMODE


_BaseMonitorEnumProc = ctypes.WINFUNCTYPE(wintypes.BOOL,
                                          wintypes.HMONITOR, wintypes.HDC, wintypes.LPRECT, wintypes.LPARAM)

_BaseEnumDisplayMonitors = function_factory(
    windll.user32.EnumDisplayMonitors,
    [wintypes.HDC, wintypes.LPRECT, _BaseMonitorEnumProc, wintypes.LPARAM],
    wintypes.BOOL,
    check_zero
)


def EnumDisplayMonitors(hdc, lpreClip, lpfnEnum, dwData):
    """
    BOOL EnumDisplayMonitors(
      HDC             hdc,
      LPCRECT         lprcClip,
      MONITORENUMPROC lpfnEnum,
      LPARAM          dwData
    );
    """
    lpfnEnum = _BaseMonitorEnumProc(lpfnEnum)
    _BaseEnumDisplayMonitors(hdc, lpreClip, lpfnEnum, dwData)


# GetMonitorInfo

_BaseGetMonitorInfoW = function_factory(
    windll.user32.GetMonitorInfoW,
    [wintypes.HMONITOR, POINTER(MONITORINFO)],
    wintypes.BOOL,
    check_zero
)

_BaseGetMonitorInfoExW = function_factory(
    windll.user32.GetMonitorInfoW,
    [wintypes.HMONITOR, POINTER(MONITORINFOEX)],
    wintypes.BOOL,
    check_zero
)


def GetMonitorInfo(hMonitor):
    """
    BOOL GetMonitorInfoW(
      HMONITOR      hMonitor,
      LPMONITORINFO lpmi
    );
    """
    py_MONITOR_INFO = MONITORINFO()
    _BaseGetMonitorInfoW(hMonitor, byref(py_MONITOR_INFO))
    return py_MONITOR_INFO


def GetMonitorInfoEx(hMonitor):
    """
    BOOL GetMonitorInfoW(
      HMONITOR      hMonitor,
      LPMONITORINFO lpmi
    );
    """
    py_MONITOR_INFO_EX = MONITORINFOEX()
    _BaseGetMonitorInfoW(hMonitor, byref(py_MONITOR_INFO_EX))
    return py_MONITOR_INFO_EX


# GetSystemMetrics

_BaseGetSystemMetrics = function_factory(
    windll.user32.GetSystemMetrics,
    [wintypes.INT],
    wintypes.INT
)


def GetSystemMetrics(nIndex):
    """
    int GetSystemMetrics(
      int nIndex
    );
    """
    return _BaseGetSystemMetrics(nIndex)
