from backend.backend import Backend
from core.list_model import ListModel
from core.signals import Signal


class MonitorProxyBackend(Backend):

    def __init__(self):
        self.__monitor_model = ListModel()

        self.monitor_model_changed = Signal()
        """Slot function signature: slot(new_model)"""

    @property
    def monitor_model(self):
        return self.__monitor_model

    @monitor_model.setter
    def monitor_model(self, value):
        self.__monitor_model = value
        self.monitor_model_changed.emit(value)
