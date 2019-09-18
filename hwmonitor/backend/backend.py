from abc import abstractmethod
from typing import Tuple

from hwmonitor.monitors.monitor_model import MonitorModel


class Backend:
    """
    The Interface for every monitor_model in this application. The Backend is used to synchronize
    the local application model with the OS provided display device model.

    The concept of the virtual screen is copied from Microsoft Windows-
    The virtual screen is the bounding rectangle of all display monitors.

    There should be no resource expensive or time consuming task in initializing the monitor model.
    A proposed solution would be returning a 'placeholder' monitor item and updating it through
    an separate thread by updating the attribute and populating the 'placeholder' step-by-step.
    """

    @abstractmethod
    def get_system_monitor_model(self) -> MonitorModel:
        """Returns a model representing the system (OS) display model
        """

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

    def finalize(self, exit_code):
        """This function is called when the application is closing.
         Use this to shutdown any existing handle to the system if needed
        """
