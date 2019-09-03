from backend.monitor_backend import BaseMonitorBackend
from core.has_properties import HasProperties, Property
from monitors.monitor import Monitor
from ui_new.align.models.view_model import AlignViewModel


class AlignModel(HasProperties):
    monitor = Property(default="")

    def __init__(self, monitor: Monitor, common_model: AlignViewModel, backend: BaseMonitorBackend):
        """Model for each AlignWidget.

        This model holds the monitor for the widget and implements its behavior.
        A memento of the current state of the monitor is created in case a rollback is needed
        """
        super().__init__()
        self.__monitor_memento = None
        self.__top_left = (0, 0)
        self.changed("monitor").connect(self.monitor_changed)

        self.monitor = monitor
        self.common_model = common_model
        self.backend = backend

    @property
    def vscreen_offset(self):
        return self.backend.get_vscreen_normalize_offset()

    @property
    def vscreen_size(self):
        return self.backend.get_vscreen_size()

    @property
    def top_left(self):
        return self.__top_left

    def monitor_changed(self, monitor: Monitor):
        self.__monitor_memento = monitor.create_memento()
        self.__top_left = monitor.position

    def rollback(self):
        self.monitor.set_memento(self.__monitor_memento)
