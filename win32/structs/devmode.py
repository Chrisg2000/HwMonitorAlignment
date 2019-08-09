import ctypes
import enum
from ctypes import wintypes

from win32.structs._base_type import _Win32BaseStruct, _Win32BaseUnion, CCHDEVICENAME, CCHFORMNAME


# noinspection PyPep8Naming,SpellCheckingInspection
class DEVICE_MODE_FIELD_FLAGS(enum.IntFlag):
    DM_ORIENTATION = 0x00000001
    DM_PAPERSIZE = 0x00000002
    DM_PAPERLENGTH = 0x00000004
    DM_PAPERWIDTH = 0x00000008
    DM_SCALE = 0x00000010
    DM_POSITION = 0x00000020
    DM_NUP = 0x00000040
    DM_DISPLAYORIENTATION = 0x00000080
    DM_COPIES = 0x00000100
    DM_DEFAULTSOURCE = 0x00000200
    DM_PRINTQUALITY = 0x00000400
    DM_COLOR = 0x00000800
    DM_DUPLEX = 0x00001000
    DM_YRESOLUTION = 0x00002000
    DM_TTOPTION = 0x00004000
    DM_COLLATE = 0x00008000
    DM_FORMNAME = 0x00010000
    DM_LOGPIXELS = 0x00020000
    DM_BITSPERPEL = 0x00040000
    DM_PELSWIDTH = 0x00080000
    DM_PELSHEIGHT = 0x00100000
    DM_DISPLAYFLAGS = 0x00200000
    DM_DISPLAYFREQUENCY = 0x00400000
    DM_ICMMETHOD = 0x00800000
    DM_ICMINTENT = 0x01000000
    DM_MEDIATYPE = 0x02000000
    DM_DITHERTYPE = 0x04000000
    DM_PANNINGWIDTH = 0x08000000
    DM_PANNINGHEIGHT = 0x10000000
    DM_DISPLAYFIXEDOUTPUT = 0x20000000


# noinspection SpellCheckingInspection
class DUMMYSTRUCTNAME(_Win32BaseStruct):
    """
    struct {
          short dmOrientation;
          short dmPaperSize;
          short dmPaperLength;
          short dmPaperWidth;
          short dmScale;
          short dmCopies;
          short dmDefaultSource;
          short dmPrintQuality;
        } DUMMYSTRUCTNAME;
    """
    _fields_ = [
        ("dmOrientation", wintypes.SHORT),
        ("dmPaperSize", wintypes.SHORT),
        ("dmPaperLength", wintypes.SHORT),
        ("dmPaperWidth", wintypes.SHORT),
        ("dmScale", wintypes.SHORT),
        ("dmCopies", wintypes.SHORT),
        ("dmDefaultSource", wintypes.SHORT),
        ("dmPrintQuality", wintypes.SHORT),
    ]


# noinspection SpellCheckingInspection
class DUMMYSTRUCTNAME2(_Win32BaseStruct):
    """
    struct {
          POINTL dmPosition;
          DWORD  dmDisplayOrientation;
          DWORD  dmDisplayFixedOutput;
        } DUMMYSTRUCTNAME2;
    """
    _fields_ = [
        ("dmPosition", wintypes.POINTL),
        ("dmDisplayOrientation", wintypes.DWORD),
        ("dmDisplayFixedOutput", wintypes.DWORD),
    ]


# noinspection SpellCheckingInspection
class DUMMYUNIONNAME(_Win32BaseUnion):
    """
    union {
        struct {
          short dmOrientation;
          short dmPaperSize;
          short dmPaperLength;
          short dmPaperWidth;
          short dmScale;
          short dmCopies;
          short dmDefaultSource;
          short dmPrintQuality;
        } DUMMYSTRUCTNAME;
        POINTL dmPosition;
        struct {
          POINTL dmPosition;
          DWORD  dmDisplayOrientation;
          DWORD  dmDisplayFixedOutput;
        } DUMMYSTRUCTNAME2;
      } DUMMYUNIONNAME;
    """
    _fields_ = [
        ("DUMMYSTRUCTNAME", DUMMYSTRUCTNAME),
        ("dmPosition", wintypes.POINTL),
        ("DUMMYSTRUCTNAME2", DUMMYSTRUCTNAME2),
    ]


# noinspection SpellCheckingInspection
class DUMMYUNIONNAME2(_Win32BaseUnion):
    """
    union {
        DWORD dmDisplayFlags;
        DWORD dmNup;
      } DUMMYUNIONNAME2;
    """
    _fields_ = [
        ("dmDisplayFlags", wintypes.DWORD),
        ("dmNup", wintypes.DWORD),
    ]


# noinspection PyTypeChecker,SpellCheckingInspection
class DEVMODE(_Win32BaseStruct):
    """https://docs.microsoft.com/en-us/windows/win32/api/wingdi/ns-wingdi-devmodew
    typedef struct _devicemodeW {
      WCHAR dmDeviceName[CCHDEVICENAME];
      WORD  dmSpecVersion;
      WORD  dmDriverVersion;
      WORD  dmSize;
      WORD  dmDriverExtra;
      DWORD dmFields;
      union {
        struct {
          short dmOrientation;
          short dmPaperSize;
          short dmPaperLength;
          short dmPaperWidth;
          short dmScale;
          short dmCopies;
          short dmDefaultSource;
          short dmPrintQuality;
        } DUMMYSTRUCTNAME;
        POINTL dmPosition;
        struct {
          POINTL dmPosition;
          DWORD  dmDisplayOrientation;
          DWORD  dmDisplayFixedOutput;
        } DUMMYSTRUCTNAME2;
      } DUMMYUNIONNAME;
      short dmColor;
      short dmDuplex;
      short dmYResolution;
      short dmTTOption;
      short dmCollate;
      WCHAR dmFormName[CCHFORMNAME];
      WORD  dmLogPixels;
      DWORD dmBitsPerPel;
      DWORD dmPelsWidth;
      DWORD dmPelsHeight;
      union {
        DWORD dmDisplayFlags;
        DWORD dmNup;
      } DUMMYUNIONNAME2;
      DWORD dmDisplayFrequency;
      DWORD dmICMMethod;
      DWORD dmICMIntent;
      DWORD dmMediaType;
      DWORD dmDitherType;
      DWORD dmReserved1;
      DWORD dmReserved2;
      DWORD dmPanningWidth;
      DWORD dmPanningHeight;
    } DEVMODEW, *PDEVMODEW, *NPDEVMODEW, *LPDEVMODEW;
    """
    _fields_ = [
        ("dmDeviceName", wintypes.WCHAR * CCHDEVICENAME),
        ("dmSpecVersion", wintypes.WORD),
        ("dmDriverVersion", wintypes.WORD),
        ("dmSize", wintypes.WORD),
        ("dmDriverExtra", wintypes.WORD),
        ("dmFields", wintypes.DWORD),
        ("DUMMYUNIONNAME", DUMMYUNIONNAME),
        ("dmColor", wintypes.SHORT),
        ("dmDuplex", wintypes.SHORT),
        ("dmYResolution", wintypes.SHORT),
        ("dmTTOption", wintypes.SHORT),
        ("dmCollate", wintypes.SHORT),
        ("dmFormName", wintypes.WCHAR * CCHFORMNAME),
        ("dmLogPixels", wintypes.WORD),
        ("dmBitsPerPel", wintypes.DWORD),
        ("dmPelsWidth", wintypes.DWORD),
        ("dmPelsHeight", wintypes.DWORD),
        ("DUMMYUNIONNAME2", DUMMYUNIONNAME2),
        ("dmDisplayFrequency", wintypes.DWORD),
        ("dmICMMethod", wintypes.DWORD),
        ("dmICMIntent", wintypes.DWORD),
        ("dmMediaType", wintypes.DWORD),
        ("dmDitherType", wintypes.DWORD),
        ("dmReserved1", wintypes.DWORD),
        ("dmReserved2", wintypes.DWORD),
        ("dmPanningWidth", wintypes.DWORD),
        ("dmPanningHeight", wintypes.DWORD),
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dmSize = ctypes.sizeof(DEVMODE)
        self.dmDriverExtra = 0
