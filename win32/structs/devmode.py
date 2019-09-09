import ctypes
from ctypes import wintypes

from win32.structs._base_type import _Win32BaseStruct, _Win32BaseUnion, CCHDEVICENAME, CCHFORMNAME


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
    _anonymous_ = ("DUMMYUNIONNAME",)
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
