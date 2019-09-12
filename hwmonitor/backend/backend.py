from abc import abstractmethod
from typing import Tuple


class Backend:

    @abstractmethod
    def get_vscreen_size(self) -> Tuple[int, int]:
        """Return the width and height of the virtual screen in pixels.

        The virtual screen is the bounding rectangle of all display monitors.
        """

    @abstractmethod
    def get_vscreen_normalize_offset(self) -> Tuple[int, int]:
        """Returns the coordinates for the top left corner of the virtual screen.

        The virtual screen is the bounding rectangle of all display monitors.
        """

    @abstractmethod
    def set_monitor_position(self, id_, x: int, y: int, *, reset=True):
        """Change the position of the monitor found under id_ on the virtual screen.

        Windows Specific:
        If reset is True the modification will take effect immediately, otherwise
        not. To let the changes take effect call this function again with None as id_.

        The virtual screen is the bounding rectangle of all display monitors.
        """
