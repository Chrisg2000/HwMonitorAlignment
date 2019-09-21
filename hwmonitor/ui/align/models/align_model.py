from hwmonitor.core.has_properties import HasProperties, Property
from hwmonitor.monitors.monitor import Monitor
from hwmonitor.ui.align.models.view_model import AlignViewModel
from hwmonitor.vscreen.vscreen import VScreen


class AlignModel(HasProperties):
    monitor = Property(default="")
    offset = Property(default=0)

    def __init__(self, monitor: Monitor, common_model: AlignViewModel, vscreen: VScreen):
        """Model for each AlignWidget.

        This model holds the monitor for the widget and implements its behavior.
        A memento of the current state of the monitor is created in case a rollback is needed
        """
        super().__init__()
        self.__monitor_memento = None
        self.changed("monitor").connect(self.monitor_changed)

        self.monitor = monitor
        self.common_model = common_model
        self.vscreen = vscreen

    @property
    def vscreen_offset(self):
        return self.vscreen.offset

    @property
    def vscreen_size(self):
        return self.vscreen.size

    def monitor_changed(self, monitor: Monitor):
        self.__monitor_memento = monitor.create_memento()

    def rollback(self):
        self.offset = 0
        self.monitor.set_memento(self.__monitor_memento)

    def apply_offset(self):
        self.monitor.position_y += self.offset
        self.offset = 0
        self.monitor.apply_changes()
