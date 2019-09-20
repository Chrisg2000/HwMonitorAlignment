from abc import abstractmethod
from typing import Tuple

from hwmonitor.core.model_adapter import ModelAdapter
from hwmonitor.monitors.monitor_model import MonitorModel


class VScreenAdapter(ModelAdapter):

    def __init__(self, model: MonitorModel):
        super().__init__(model)

    @property
    def model(self) -> MonitorModel:
        return self._model

    @abstractmethod
    def get_primary_monitor(self):
        """Returns the monitor which has primary flag set"""

    @abstractmethod
    def get_monitor_order(self):
        """Yields the display monitors in order on the virtual screen
        from left to right, top to bottom.

        The virtual screen is the bounding rectangle of all display monitors.
        """

    @abstractmethod
    def get_from_position(self, x, y):
        """Returns the monitor which includes the given position on the virtual screen.
        If supplied position is outside of visible virtual screen area a LookupError will be raised.

        The virtual screen is the bounding rectangle of all display monitors.
        """

    @abstractmethod
    def get_vscreen_size(self):
        """Return the width and height of the virtual screen in pixels.

        The virtual screen is the bounding rectangle of all display monitors.
        """

    @abstractmethod
    def get_vscreen_normalize_offset(self) -> Tuple[int, int]:
        """Returns the coordinates for the top left corner of the virtual screen.

        The virtual screen is the bounding rectangle of all display monitors.
        """
