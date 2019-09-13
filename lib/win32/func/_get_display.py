from ctypes import windll, POINTER, byref, wintypes

from lib.win32._util import function_factory, check_zero
from lib.win32.structs import MONITORINFO, MONITORINFOEX

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
    The GetMonitorInfo_ function retrieves information about a display monitor.

    .. code:: c
        BOOL GetMonitorInfoW(
          HMONITOR      hMonitor,
          LPMONITORINFO lpmi
        );

    .. _GetMonitorInfo: https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-getmonitorinfow
    :param hMonitor: A handle to the display monitor of interest.
    :return: MONITORINFO structure that received information about the specified display monitor
    :raises WindowsError: If the function succeeds, the return value is nonzero.
    """
    py_MONITOR_INFO = MONITORINFO()
    _BaseGetMonitorInfoW(hMonitor, byref(py_MONITOR_INFO))
    return py_MONITOR_INFO


def GetMonitorInfoEx(hMonitor):
    """
    The GetMonitorInfo_ function retrieves information about a display monitor.

    .. code:: c
        BOOL GetMonitorInfoW(
          HMONITOR      hMonitor,
          LPMONITORINFO lpmi
        );

    .. _GetMonitorInfo: https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-getmonitorinfow
    :param hMonitor: A handle to the display monitor of interest.
    :return: MONITORINFOEX structure that received information about the specified display monitor
    :raises WindowsError: If the function succeeds, the return value is nonzero.
    """
    py_MONITOR_INFO_EX = MONITORINFOEX()
    _BaseGetMonitorInfoW(hMonitor, byref(py_MONITOR_INFO_EX))
    return py_MONITOR_INFO_EX
