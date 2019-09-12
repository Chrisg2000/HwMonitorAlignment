from abc import abstractmethod
from collections import Sized, Iterable, Container

from hwmonitor.core.signals import Signal


class Model(Sized, Iterable, Container):

    def __init__(self):
        self.item_added = Signal()
        """Slot function signature: slot(index, item)"""
        self.item_removed = Signal()
        """Slot function signature: slot(index, item)"""
        self.model_reset = Signal()
        """Slot function signature: slot()"""

    @abstractmethod
    def add(self, item):
        pass

    @abstractmethod
    def remove(self, item):
        pass

    @abstractmethod
    def reset(self):
        pass
