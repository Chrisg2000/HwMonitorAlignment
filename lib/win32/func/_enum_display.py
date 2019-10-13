import ctypes
from ctypes import windll, POINTER, byref, wintypes

from lib.win32._util import function_factory, check_zero
from lib.win32.structs import DISPLAY_DEVICE, DEVMODE

# EnumDisplayDevices
_BaseEnumDisplayDevices = function_factory(
    windll.user32.EnumDisplayDevicesW,
    [wintypes.LPCWSTR, wintypes.DWORD, POINTER(DISPLAY_DEVICE), wintypes.DWORD],
    wintypes.BOOL,
    check_zero)


def EnumDisplayDevices(lpDevice, iDevNum, dwFlags):
    """
    The EnumDisplayDevices_ function lets you obtain information about the display devices in the current session.

    .. code:: c
        BOOL EnumDisplayDevicesW(
          LPCWSTR          lpDevice,
          DWORD            iDevNum,
          PDISPLAY_DEVICEW lpDisplayDevice,
          DWORD            dwFlags
        );

    .. _EnumDisplayDevices: https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-enumdisplaydevicesw

    :param lpDevice: A pointer to the device name.
    :param iDevNum: An index value that specifies the display device of interest.
    :param dwFlags: Flags
    :return: DISPLAY_DEVICE structure that received information about the display device specified by iDevNum.
    :raises WindowsError: If the function succeeds, the return value is nonzero.
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
    The EnumDisplaySettings_ function retrieves information about one of the graphics modes for a display device.
    To retrieve information for all the graphics modes of a display device, make a series of calls to this function.

    .. code:: c
        BOOL EnumDisplaySettingsW(
          LPCWSTR  lpszDeviceName,
          DWORD    iModeNum,
          DEVMODEW *lpDevMode
        );

    .. _EnumDisplaySettings: https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-enumdisplaysettingsw

    :param lpszDeviceName: A pointer to a null-terminated string that specifies the display device about whose
    graphics mode the function will obtain information.
    :param iModeNum: The type of information to be retrieved.
    :return: DEVMODE structure into which the function stored information about the specified graphics mode
    :raises WindowsError: If the function succeeds, the return value is nonzero.
    """
    py_DEVMODE = DEVMODE()
    _BaseEnumDisplaySettings(lpszDeviceName, iModeNum, byref(py_DEVMODE))
    return py_DEVMODE


# EnumDisplayMonitors

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
    The EnumDisplayMonitors_ function enumerates display monitors (including invisible pseudo-monitors associated with
    the mirroring drivers) that intersect a region formed by the intersection of a specified clipping rectangle and
    the visible region of a device context. EnumDisplayMonitors calls an application-defined MonitorEnumProc_ callback
    function once for each monitor that is enumerated. Note that GetSystemMetrics_ (SM_CMONITORS)
    counts only the display monitors.

    .. code:: c
        BOOL EnumDisplayMonitors(
          HDC             hdc,
          LPCRECT         lprcClip,
          MONITORENUMPROC lpfnEnum,
          LPARAM          dwData
        );

    .. _EnumDisplayMonitors: https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-enumdisplaymonitors
    .. _MonitorEnumProc: https://docs.microsoft.com/de-de/windows/win32/api/winuser/nc-winuser-monitorenumproc
    .. _GetSystemMetrics: https://docs.microsoft.com/de-de/windows/win32/api/winuser/nf-winuser-getsystemmetrics

    :param hdc: A handle to a display device context that defines the visible region of interest.
    :param lpreClip: A pointer to a RECT structure that specifies a clipping rectangle
    :param lpfnEnum: A pointer to a MonitorEnumProc application-defined callback function.
    :param dwData: Application-defined data that EnumDisplayMonitors passes directly to the MonitorEnumProc function.
    :raises WindowsError: If the function succeeds, the return value is nonzero.
    """
    lpfnEnum = _BaseMonitorEnumProc(lpfnEnum)
    _BaseEnumDisplayMonitors(hdc, lpreClip, lpfnEnum, dwData)
