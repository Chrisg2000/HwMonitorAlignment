import ctypes

# noinspection SpellCheckingInspection
CCHDEVICENAME = 32
# noinspection SpellCheckingInspection
CCHFORMNAME = 32


# noinspection SpellCheckingInspection
class _Win32BaseStruct(ctypes.Structure):
    _fields_ = []

    def __str__(self):
        return "{}: {{{}}}".format(self.__class__.__name__, ", ".join(
            ["{}: {}".format(field[0], getattr(self, field[0]))
             for field in self._fields_]))


# noinspection SpellCheckingInspection
class _Win32BaseUnion(ctypes.Union):
    _fields_ = []

    def __str__(self):
        return "{}: {{{}}}".format(self.__class__.__name__, ", ".join(
            ["{}: {}".format(field[0], getattr(self, field[0]))
             for field in self._fields_]))
