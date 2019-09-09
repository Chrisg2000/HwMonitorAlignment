from ctypes import windll, wintypes, POINTER, byref

from win32._util import function_factory
from win32.structs.devmode import DEVMODE

_BaseChangeDisplaySettingsEx = function_factory(
    windll.user32.ChangeDisplaySettingsExW,
    [wintypes.LPCWSTR, POINTER(DEVMODE), wintypes.HWND, wintypes.DWORD, wintypes.LPVOID],
    wintypes.LONG,
    None
)


def ChangeDisplaySettingsEx(lpszDeviceName, lpDevMode, dwflags, lParam=None):
    """
    The ChangeDisplaySettingsEx_ function changes the settings of the specified display
    device to the specified graphics mode.

    .. code:: c
        LONG ChangeDisplaySettingsExW(
          LPCWSTR  lpszDeviceName,
          DEVMODEW *lpDevMode,
          HWND     hwnd,
          DWORD    dwflags,
          LPVOID   lParam
        );

    .. _ChangeDisplaySettingsEx: https://docs.microsoft.com/windows/win32/api/winuser/nf-winuser-changedisplaysettingsexw
    .. _DEVMODE: https://docs.microsoft.com/windows/win32/api/wingdi/ns-wingdi-devmodew

    :param lpszDeviceName: A pointer to a null-terminated string that specifies the display device
    whose graphics mode will change
    :param lpDevMode: A pointer to a DEVMODE_ structure that describes the new graphics mode
    :param dwflags: Indicates how the graphics mode should be changed
    :param lParam: If dwFlags is CDS_VIDEOPARAMETERS, lParam is a pointer to a VIDEOPARAMETERS structure
    :return: The ChangeDisplaySettingsEx_ function returns one of the following values
    """
    p_lpDevMode = byref(lpDevMode) if lpDevMode else None
    return _BaseChangeDisplaySettingsEx(lpszDeviceName, p_lpDevMode, None, dwflags, lParam)
