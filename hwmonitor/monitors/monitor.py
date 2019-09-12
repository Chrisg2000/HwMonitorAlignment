import enum
from typing import Tuple

from hwmonitor.core.has_properties import HasProperties, Property, WriteOnceProperty
from hwmonitor.core.memento import Memento


# noinspection SpellCheckingInspection
class DisplayOrientation(enum.IntEnum):
    DMDO_DEFAULT = 0
    DMDO_90 = 1
    DMDO_180 = 2
    DMDO_270 = 3


class Monitor(HasProperties, Memento):
    device_name = WriteOnceProperty(default='')
    monitor_name = Property(default='')
    friendly_monitor_name = Property(default='')
    display_adapter = Property(default='')

    screen_width = Property(default=0)
    screen_height = Property(default=0)
    position_x = Property(default=0)
    position_y = Property(default=0)
    orientation = Property(default=DisplayOrientation.DMDO_DEFAULT)

    primary = Property(default=False)

    @property
    def aspect_ratio(self) -> float:
        if self.screen_height == 0:
            raise ValueError("Invalid Monitor defined. Impossible size of height = 0")
        return self.screen_width / self.screen_height

    def __init__(self,
                 device_name='',
                 monitor_name='',
                 friendly_monitor_name='',
                 display_adapter='',
                 screen_width=0,
                 screen_height=0,
                 position_x=0,
                 position_y=0,
                 orientation=DisplayOrientation.DMDO_DEFAULT,
                 primary=False):
        super().__init__()
        self.device_name = device_name
        self.monitor_name = monitor_name
        self.friendly_monitor_name = friendly_monitor_name
        self.display_adapter = display_adapter

        self.screen_width = screen_width
        self.screen_height = screen_height
        self.position_x = position_x
        self.position_y = position_y
        self.orientation = orientation

        self.primary = primary

    @property
    def position(self) -> Tuple[float, float]:
        return self.position_x, self.position_y

    @property
    def size(self) -> Tuple[int, int]:
        return self.screen_width, self.screen_height

    def create_memento(self):
        return (self.device_name,
                self.monitor_name,
                self.friendly_monitor_name,
                self.display_adapter,
                self.screen_width,
                self.screen_height,
                self.position_x,
                self.position_y,
                self.orientation,
                self.primary)

    def set_memento(self, memento):
        (self.device_name,
         self.monitor_name,
         self.friendly_monitor_name,
         self.display_adapter,
         self.screen_width,
         self.screen_height,
         self.position_x,
         self.position_y,
         self.orientation,
         self.primary) = memento

    @classmethod
    def from_memento(cls, memento):
        monitor = Monitor()
        monitor.set_memento(memento)
        return monitor

    def __str__(self):
        return f"device_name: {self.device_name} " \
               f"monitor_name: {self.monitor_name} " \
               f"friendly_monitor_name: {self.friendly_monitor_name} " \
               f"display_adapter: {self.display_adapter} " \
               f"screen_width: {self.screen_width} " \
               f"screen_height: {self.screen_height} " \
               f"position_x: {self.position_x} " \
               f"position_y: {self.position_y} " \
               f"orientation: {self.orientation} " \
               f"primary: {self.primary}"
