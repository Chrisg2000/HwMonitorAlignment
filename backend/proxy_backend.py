from typing import Tuple

from backend.backend import Backend
from core.signals import Signal


class ProxyBackend(Backend):
    def __init__(self, backend: Backend):
        super().__init__()
        self.__backend = backend

        self.backend_changed = Signal()
        """Slot function signature: slot(new_backend)"""

    @property
    def backend(self):
        return self.__backend

    @backend.setter
    def backend(self, value):
        self.__backend = value
        self.backend_changed.emit(value)

    def get_vscreen_size(self) -> Tuple[int, int]:
        return self.backend.get_vscreen_size()

    def get_vscreen_normalize_offset(self) -> Tuple[int, int]:
        return self.backend.get_vscreen_normalize_offset()

    def __getattr__(self, item):
        try:
            attr = getattr(self.backend, item)
            _ = attr
        except (AttributeError, NameError):
            raise AttributeError()
        else:
            if callable(attr):
                def method(*args, **kwargs):
                    return attr(*args, **kwargs)

                return method
            else:
                return attr
