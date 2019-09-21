from typing import Iterator

from hwmonitor.core.model import Model
from hwmonitor.monitors.monitor import Monitor


class MonitorModel(Model):
    """Simple model to store monitor objects by their device name
     as (monitor.device_name, monitor) pairs

    The model can be iterated to retrieve the monitors, to get the monitor device name pairs,
    use the items() method, to get only the device_names use keys() method.
    """

    def __init__(self):
        super().__init__()

        self.__monitors = {}

    def add(self, monitor: Monitor):
        if monitor.device_name in self.__monitors:
            raise ValueError("Monitor is already in the model")

        self.__monitors[monitor.device_name] = monitor
        self.item_added.emit(monitor.device_name, monitor)

    def remove(self, monitor: Monitor):
        self.pop(monitor.device_name)

    def pop(self, device_name: str):
        monitor = self.__monitors.pop(device_name)
        self.item_removed.emit(device_name, monitor)

        return monitor

    def get(self, device_name, default=None):
        return self.__monitors.get(device_name, default)

    def items(self):
        """Returns a set-like object providing a view on model items (device_name, monitor)"""
        return self.__monitors.items()

    def keys(self):
        """Return a set-like object providing a view of model keys (device_name)"""
        return self.__monitors.keys()

    def reset(self):
        self.__monitors.clear()
        self.model_reset.emit()

    def filter(self, operation):
        """Returns a generator over monitors for which operation yields True
        """
        for monitor in self.__monitors.values():
            if operation(monitor):
                yield monitor

    def __len__(self) -> int:
        return len(self.__monitors)

    def __iter__(self) -> Iterator[Monitor]:
        return self.__monitors.values().__iter__()

    def __contains__(self, x: object) -> bool:
        return x in self.__monitors
