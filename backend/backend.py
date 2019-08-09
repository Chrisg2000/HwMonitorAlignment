from abc import abstractmethod
from typing import Tuple

from core.list_model import ListModel


class Backend:

    def __init__(self):
        self._monitor_model = ListModel()

    @property
    def monitor_model(self):
        return self._monitor_model

    @abstractmethod
    def get_monitor_model(self) -> ListModel:
        pass

    @abstractmethod
    def get_vscreen_size(self) -> Tuple[int, int]:
        pass

    @abstractmethod
    def get_vscreen_normalize_offset(self) -> Tuple[int, int]:
        pass
