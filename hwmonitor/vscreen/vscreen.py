from abc import abstractmethod
from typing import Tuple

from hwmonitor.core.signals import Signal
from hwmonitor.monitors.monitor import Monitor
from hwmonitor.monitors.monitor_model import MonitorModel


class VScreen:

    def __init__(self, monitors: MonitorModel):
        super().__init__()

        self._monitors = monitors

        self.layout_changed = Signal()
        self.monitor_added = Signal()
        self.monitor_removed = Signal()
        self.monitor_model_reset = Signal()

        self._monitors.item_added.connect(self.monitor_added.emit)
        self._monitors.item_removed.connect(self.monitor_removed.emit)
        self._monitors.model_reset.connect(self.monitor_model_reset.emit)

    @property
    def monitors(self) -> MonitorModel:
        return self._monitors

    @property
    @abstractmethod
    def primary_monitor(self) -> Monitor:
        """Returns the monitor which has primary flag set"""

    @property
    @abstractmethod
    def monitor_order(self):
        """Yields the display _monitors in order on the virtual screen
        from left to right, top to bottom.

        The virtual screen is the bounding rectangle of all display _monitors.
        """

    @property
    @abstractmethod
    def size(self) -> Tuple[int, int]:
        """Return the width and height of the virtual screen in pixels.

        The virtual screen is the bounding rectangle of all display _monitors.
        """

    @property
    @abstractmethod
    def offset(self) -> Tuple[int, int]:
        """Returns the coordinates for the top left corner of the virtual screen.

        The virtual screen is the bounding rectangle of all display _monitors.
        """

    @abstractmethod
    def get_from_position(self, x, y) -> Monitor:
        """Returns the monitor which includes the given position on the virtual screen.
        If supplied position is outside of visible virtual screen area a LookupError will be raised.

        The virtual screen is the bounding rectangle of all display _monitors.
        """

    @abstractmethod
    def apply_changes(self):
        """Apply the modification to the system. This method should inform the underlying
        system that the layout of the monitors on the virtual screen has changes.
        This may not be required, depending on the implementation of monitor.

        If this function is called the layout_changed signal should be emitted.
        """
