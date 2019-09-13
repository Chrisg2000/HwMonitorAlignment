from ctypes import c_uint32, c_uint16, c_bool, c_char
from ctypes.wintypes import WCHAR

from lib.win32.structs._base_type import _Win32BaseStruct, c_enum, LUID, CCHDEVICENAME


class DISPLAYCONFIG_DEVICE_INFO_HEADER(_Win32BaseStruct):
    """
    typedef struct DISPLAYCONFIG_DEVICE_INFO_HEADER {
      DISPLAYCONFIG_DEVICE_INFO_TYPE type;
      UINT32                         size;
      LUID                           adapterId;
      UINT32                         id;
    } DISPLAYCONFIG_DEVICE_INFO_HEADER;
    """
    _fields_ = [
        ("type", c_enum),
        ("size", c_uint32),
        ("adapterId", LUID),
        ("id", c_uint32),
    ]


class DISPLAYCONFIG_TARGET_DEVICE_NAME(_Win32BaseStruct):
    """
    typedef struct DISPLAYCONFIG_TARGET_DEVICE_NAME {
      DISPLAYCONFIG_DEVICE_INFO_HEADER       header;
      DISPLAYCONFIG_TARGET_DEVICE_NAME_FLAGS flags;
      DISPLAYCONFIG_VIDEO_OUTPUT_TECHNOLOGY  outputTechnology;
      UINT16                                 edidManufactureId;
      UINT16                                 edidProductCodeId;
      UINT32                                 connectorInstance;
      WCHAR                                  monitorFriendlyDeviceName[64];
      WCHAR                                  monitorDevicePath[128];
    } DISPLAYCONFIG_TARGET_DEVICE_NAME;
    """
    _fields_ = [
        ("header", DISPLAYCONFIG_DEVICE_INFO_HEADER),
        ("flags", c_uint32),
        ("outputTechnology", c_enum),
        ("edidManufactureId", c_uint16),
        ("edidProductCodeId", c_uint16),
        ("connectorInstance", c_uint32),
        ("monitorFriendlyDeviceName", WCHAR * 64),
        ("monitorDevicePath", WCHAR * 128),
    ]


class DISPLAYCONFIG_SOURCE_DEVICE_NAME(_Win32BaseStruct):
    """
    typedef struct DISPLAYCONFIG_SOURCE_DEVICE_NAME {
      DISPLAYCONFIG_DEVICE_INFO_HEADER header;
      WCHAR                            viewGdiDeviceName[CCHDEVICENAME];
    } DISPLAYCONFIG_SOURCE_DEVICE_NAME;
    """
    _fields_ = [
        ("header", DISPLAYCONFIG_DEVICE_INFO_HEADER),
        ("viewGdiDeviceName", WCHAR * CCHDEVICENAME),
    ]


class DISPLAYCONFIG_ADAPTER_NAME(_Win32BaseStruct):
    """
    typedef struct DISPLAYCONFIG_ADAPTER_NAME {
      DISPLAYCONFIG_DEVICE_INFO_HEADER header;
      WCHAR                            adapterDevicePath[128];
    } DISPLAYCONFIG_ADAPTER_NAME;
    """
    _fields_ = [
        ("header", DISPLAYCONFIG_DEVICE_INFO_HEADER),
        ("adapterDevicePath", WCHAR * 128),
    ]


class DISPLAYCONFIG_PATH_SOURCE_INFO(_Win32BaseStruct):
    """
    typedef struct DISPLAYCONFIG_PATH_SOURCE_INFO {
      LUID   adapterId;
      UINT32 id;
      union {
        UINT32 modeInfoIdx;
        struct {
          UINT32 cloneGroupId : 16;
          UINT32 sourceModeInfoIdx : 16;
        } DUMMYSTRUCTNAME;
      } DUMMYUNIONNAME;
      UINT32 statusFlags;
    } DISPLAYCONFIG_PATH_SOURCE_INFO;
    """
    _fields_ = [
        ("adapterId", LUID),
        ("id", c_uint32),
        ("modeInfoIdx", c_uint32),
        ("statusFlags", c_uint32),
    ]


class DISPLAYCONFIG_RATIONAL(_Win32BaseStruct):
    """
    typedef struct DISPLAYCONFIG_RATIONAL {
      UINT32 Numerator;
      UINT32 Denominator;
    } DISPLAYCONFIG_RATIONAL;
    """
    _fields_ = [
        ("Numerator", c_uint32),
        ("Denominator", c_uint32)
    ]


class DISPLAYCONFIG_PATH_TARGET_INFO(_Win32BaseStruct):
    """
    typedef struct DISPLAYCONFIG_PATH_TARGET_INFO {
      LUID                                  adapterId;
      UINT32                                id;
      union {
        UINT32 modeInfoIdx;
        struct {
          UINT32 desktopModeInfoIdx : 16;
          UINT32 targetModeInfoIdx : 16;
        } DUMMYSTRUCTNAME;
      } DUMMYUNIONNAME;
      DISPLAYCONFIG_VIDEO_OUTPUT_TECHNOLOGY outputTechnology;
      DISPLAYCONFIG_ROTATION                rotation;
      DISPLAYCONFIG_SCALING                 scaling;
      DISPLAYCONFIG_RATIONAL                refreshRate;
      DISPLAYCONFIG_SCANLINE_ORDERING       scanLineOrdering;
      BOOL                                  targetAvailable;
      UINT32                                statusFlags;
    } DISPLAYCONFIG_PATH_TARGET_INFO;
    """
    _fields_ = [
        ("adapterId", LUID),
        ("id", c_uint32),
        ("modeInfoIdx", c_uint32),
        ("outputTechnology", c_enum),
        ("rotation", c_enum),
        ("scaling", c_enum),
        ("refreshRate", DISPLAYCONFIG_RATIONAL),
        ("scanLineOrdering", c_enum),
        ("targetAvailable", c_bool),
        ("statusFlags", c_uint32),
    ]


class DISPLAYCONFIG_PATH_INFO(_Win32BaseStruct):
    """
    typedef struct DISPLAYCONFIG_PATH_INFO {
      DISPLAYCONFIG_PATH_SOURCE_INFO sourceInfo;
      DISPLAYCONFIG_PATH_TARGET_INFO targetInfo;
      UINT32                         flags;
    } DISPLAYCONFIG_PATH_INFO;
    """
    _fields_ = [
        ("sourceInfo", DISPLAYCONFIG_PATH_SOURCE_INFO),
        ("targetInfo", DISPLAYCONFIG_PATH_TARGET_INFO),
        ("flags", c_uint32),
    ]


# noinspection PyTypeChecker
class DISPLAYCONFIG_MODE_INFO(_Win32BaseStruct):
    """
    typedef struct DISPLAYCONFIG_MODE_INFO {
      DISPLAYCONFIG_MODE_INFO_TYPE infoType;
      UINT32                       id;
      LUID                         adapterId;
      union {
        DISPLAYCONFIG_TARGET_MODE        targetMode;
        DISPLAYCONFIG_SOURCE_MODE        sourceMode;
        DISPLAYCONFIG_DESKTOP_IMAGE_INFO desktopImageInfo;
      } DUMMYUNIONNAME;
    } DISPLAYCONFIG_MODE_INFO;
    """
    _fields_ = [
        ("infoType", c_enum),
        ("id", c_uint32),
        ("adapterId", LUID),
        ("modeInfo", c_char * 48),  # otherwise huge overhead of structs
    ]
