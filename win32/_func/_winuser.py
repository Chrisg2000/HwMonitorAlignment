import ctypes
from ctypes import windll, POINTER, byref, wintypes

from win32._util import function_factory, check_zero
from win32.structs.devmode import DEVMODE
from win32.structs.display_device import DISPLAY_DEVICE

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
