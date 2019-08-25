from abc import ABC

from backend.backend import Backend
from monitors.monitor_model import MonitorModel
from core.signals import Signal


class BaseMonitorBackend(Backend, ABC):

    def __init__(self):
        self.__monitor_model = MonitorModel()

        self.monitor_added = Signal()
        self.monitor_removed = Signal()
        self.monitor_model_reset = Signal()

        self.__monitor_model.item_added.connect(self._monitor_added)
        self.__monitor_model.item_removed.connect(self._monitor_removed)
        self.__monitor_model.model_reset.connect(self._monitor_model_reset)

    @property
    def monitor_model(self):
        return self.__monitor_model

    def _monitor_added(self, index, item):
        self.monitor_added.emit(index, item)

    def _monitor_removed(self, index, item):
        self.monitor_removed.emit(index, item)

    def _monitor_model_reset(self):
        self.monitor_model_reset.emit()
