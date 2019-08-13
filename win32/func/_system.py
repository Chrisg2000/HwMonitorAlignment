from ctypes import windll, wintypes

from win32._util import function_factory

# GetSystemMetrics

_BaseGetSystemMetrics = function_factory(
    windll.user32.GetSystemMetrics,
    [wintypes.INT],
    wintypes.INT
)


def GetSystemMetrics(nIndex):
    """
    Retrieves the specified system metric or system configuration setting.
    Note that all dimensions retrieved by GetSystemMetrics_ are in pixels.

    .. code:: c
        int GetSystemMetrics(
          int nIndex
        );

    .. _GetSystemMetrics: https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-getsystemmetrics

    :param nIndex: The system metric or configuration setting to be retrieved
    :return:  the return value is the requested system metric or configuration setting.
    """
    return _BaseGetSystemMetrics(nIndex)
