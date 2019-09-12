import ctypes
from ctypes import windll, c_uint32, wintypes, POINTER, byref
from typing import Any

from hwmonitor.win32._util import function_factory, check_rcode
from hwmonitor.win32.structs.displayconfig import DISPLAYCONFIG_PATH_INFO, DISPLAYCONFIG_MODE_INFO, \
    DISPLAYCONFIG_DEVICE_INFO_HEADER

_BaseGetDisplayConfigBufferSizes = function_factory(
    windll.user32.GetDisplayConfigBufferSizes,
    [c_uint32, POINTER(c_uint32), POINTER(c_uint32)],
    wintypes.LONG,
    check_rcode
)


def GetDisplayConfigBufferSizes(flags):
    """
    The GetDisplayConfigBufferSizes_ function retrieves the size of the buffers that are required
    to call the QueryDisplayConfig_ function.

    .. code:: c
        LONG GetDisplayConfigBufferSizes(
          UINT32 flags,
          UINT32 *numPathArrayElements,
          UINT32 *numModeInfoArrayElements
        );

    .. _QueryDisplayConfig: https://docs.microsoft.com/windows/desktop/api/winuser/nf-winuser-querydisplayconfig
    .. _GetDisplayConfigBufferSizes: https://docs.microsoft.com/windows/win32/api/winuser/nf-winuser-getdisplayconfigbuffersizes

    :param flags: The type of information to retrieve.
    :returns:
        - numPathArrayElements - variable that receives the number of elements in the path information table
        - numModeInfoArrayElements -  variable that receives the number of elements in the mode information table
    :raises WindowsError: If the function returns an error code
    """
    py_numPathArrayElements = c_uint32()
    py_numModeInfoArrayElements = c_uint32()
    _BaseGetDisplayConfigBufferSizes(flags, byref(py_numPathArrayElements), byref(py_numModeInfoArrayElements))
    return py_numPathArrayElements, py_numModeInfoArrayElements


_BaseQueryDisplayConfig = function_factory(
    windll.user32.QueryDisplayConfig,
    [c_uint32, POINTER(c_uint32), POINTER(DISPLAYCONFIG_PATH_INFO), POINTER(c_uint32), POINTER(DISPLAYCONFIG_MODE_INFO),
     POINTER(c_uint32)],
    wintypes.LONG,
    check_rcode
)


def QueryDisplayConfig(flags, numPathArrayElements, numModeInfoArrayElements):
    """
    The QueryDisplayConfig_ function retrieves information about all possible display paths for all display devices,
    or views, in the current setting.

    .. code:: c
        LONG QueryDisplayConfig(
          UINT32                    flags,
          UINT32                    *numPathArrayElements,
          DISPLAYCONFIG_PATH_INFO   *pathArray,
          UINT32                    *numModeInfoArrayElements,
          DISPLAYCONFIG_MODE_INFO   *modeInfoArray,
          DISPLAYCONFIG_TOPOLOGY_ID *currentTopologyId
        );

    .. _QueryDisplayConfig: https://docs.microsoft.com/windows/desktop/api/winuser/nf-winuser-querydisplayconfig

    :param flags: The type of information to retrieve
    :param numPathArrayElements: variable that contains the number of elements in pPathInfoArray
    :param numModeInfoArrayElements: variable that specifies the number in element of the mode information table
    :returns:
        - displayPaths - variable that contains an array of DISPLAYCONFIG_PATH_INFO elements
        - displayModes - variable that contains an array of DISPLAYCONFIG_MODE_INFO elements
    :raises WindowsError: If the function returns an error code
    """
    py_displayPaths = (DISPLAYCONFIG_PATH_INFO * numPathArrayElements.value)()
    py_displayModes = (DISPLAYCONFIG_MODE_INFO * numModeInfoArrayElements.value)()

    _BaseQueryDisplayConfig(flags,
                            byref(numPathArrayElements),
                            ctypes.cast(py_displayPaths, POINTER(DISPLAYCONFIG_PATH_INFO)),
                            byref(numModeInfoArrayElements),
                            ctypes.cast(py_displayModes, POINTER(DISPLAYCONFIG_MODE_INFO)),
                            None)
    return py_displayPaths, py_displayModes


_BaseDisplayConfigGetDeviceInfo = function_factory(
    windll.user32.DisplayConfigGetDeviceInfo,
    [POINTER(DISPLAYCONFIG_DEVICE_INFO_HEADER)],
    wintypes.LONG,
    check_rcode
)


def DisplayConfigGetDeviceInfo(target: Any, type_, adapterId, id_):
    """
    The DisplayConfigGetDeviceInfo_ function retrieves display configuration information about the device.

    .. note::
        This function behaves differently than others!
        A user supplied argument (target) will be changed, it does not return a new instance!

    .. code:: c
        LONG DisplayConfigGetDeviceInfo(
          DISPLAYCONFIG_DEVICE_INFO_HEADER *requestPacket
        );

    .. _DisplayConfigGetDeviceInfo: https://docs.microsoft.com/windows/win32/api/winuser/nf-winuser-displayconfiggetdeviceinfo

    :param target: Contains information about the request, which includes the packet type in the type member.
    :param type_: A DISPLAYCONFIG_DEVICE_INFO_TYPE enumerated value that determines the type of device information
     to retrieve or set
    :param adapterId: A locally unique identifier (LUID) that identifies the adapter that the device
     information packet refers to.
    :param id_: The source or target identifier to get or set the device information for.
    :raises WindowsError: If the function returns an error code
    """
    target.header = DISPLAYCONFIG_DEVICE_INFO_HEADER(
        type=type_,
        size=ctypes.sizeof(target),
        adapterId=adapterId,
        id=id_
    )

    _BaseDisplayConfigGetDeviceInfo(byref(target.header))
