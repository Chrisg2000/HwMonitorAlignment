import ctypes
from ctypes import wintypes

CCHDEVICENAME = 32
CCHFORMNAME = 32
c_enum = ctypes.c_uint32


class _Win32BaseStruct(ctypes.Structure):
    _fields_ = []

    def __str__(self):
        return "{}: {{{}}}".format(self.__class__.__name__, ", ".join(
            ["{}: {}".format(field[0], getattr(self, field[0]))
             for field in self._fields_]))


class _Win32BaseUnion(ctypes.Union):
    _fields_ = []

    def __str__(self):
        return "{}: {{{}}}".format(self.__class__.__name__, ", ".join(
            ["{}: {}".format(field[0], getattr(self, field[0]))
             for field in self._fields_]))


class LUID(_Win32BaseStruct):
    """
    typedef struct _LUID {
      DWORD LowPart;
      LONG  HighPart;
    } LUID, *PLUID;
    """
    _fields_ = [
        ("LowPart", wintypes.DWORD),
        ("HighPart", wintypes.LONG),
    ]
