import ctypes
from ctypes import wintypes

from core.memento import Memento

CCHDEVICENAME = 32
CCHFORMNAME = 32
c_enum = ctypes.c_uint32


class __Memento(Memento):
    def create_memento(self: ctypes.Structure):
        return bytes(self)

    def set_memento(self, memento):
        ctypes.memmove(
            ctypes.addressof(self),
            memento,
            ctypes.sizeof(self))

    @classmethod
    def from_memento(cls: ctypes.Structure, memento):
        return cls.from_buffer_copy(memento)


class _Win32BaseStruct(__Memento, ctypes.Structure):
    _fields_ = []

    def __str__(self):
        return "{}: {{{}}}".format(self.__class__.__name__, ", ".join(
            ["{}: {}".format(field[0], getattr(self, field[0]))
             for field in self._fields_]))


class _Win32BaseUnion(__Memento, ctypes.Union):
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
