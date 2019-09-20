from abc import abstractmethod
from typing import Tuple

from hwmonitor.vscreen.vscreen import VScreen


class Backend:
    """
    The Interface for communicating with the system. The backend is used to fill
    the local application vscreen model with the OS provided display device data

    The concept of the virtual screen is copied from Microsoft Windows -
    The virtual screen is the bounding rectangle of all display monitors.

    VScreen and Monitor should be connected to the backend, since they should
    not talk with the system on their own.
    """

    @abstractmethod
    def get_vscreen(self) -> VScreen:
        """Returns a model representing the system (OS) vscreen
        """

    @abstractmethod
    def get_vscreen_size(self) -> Tuple[int, int]:
        """Return the width and height of the virtual screen in pixels.

        The virtual screen is the bounding rectangle of all display _monitors.
        """

    @abstractmethod
    def get_vscreen_offset(self) -> Tuple[int, int]:
        """Returns the coordinates for the top left corner of the virtual screen.

        The virtual screen is the bounding rectangle of all display _monitors.
        """

    @abstractmethod
    def set_monitor_position(self, id_, x: int, y: int, *, reset=True):
        """Change the position of the monitor found under id_ on the virtual screen.

        Windows Specific:
        If reset is True the modification will take effect immediately, otherwise
        not. To let the changes take effect call this function again with None as id_.

        The virtual screen is the bounding rectangle of all display _monitors.
        """

    def finalize(self, exit_code):
        """This function is called when the application is closing.
         Use this to shutdown any existing handle to the system if needed
        """
