from core.has_properties import HasProperties, Property
from monitors.monitor import Monitor


class AlignModel(HasProperties):
    monitor = Property(default="")

    def __init__(self, monitor: Monitor):
        """Model for each AlignWidget.

        This model holds the monitor for the widget and implements its behavior.
        A memento of the current state of the monitor is created in case a rollback is needed
        """
        super().__init__()
        self.__monitor_memento = None
        self.changed("monitor").connect(self.monitor_changed)

        self.monitor = monitor

    def monitor_changed(self, monitor: Monitor):
        self.__monitor_memento = monitor.create_memento()

    def rollback(self):
        self.monitor.set_memento(self.__monitor_memento)
