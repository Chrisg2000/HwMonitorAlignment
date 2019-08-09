from typing import Tuple

from backend.monitor_backend import MonitorProxyBackend
from core.monitor_model import MonitorModel


class DebugBackend(MonitorProxyBackend):

    def __init__(self):
        super().__init__()

        self.__vscreen_size = (0, 0)
        self.__vscreen_normalize_offset = (0, 0)

        self.monitor_model_changed.connect(self._changed_monitor_model)

    def get_vscreen_size(self) -> Tuple[int, int]:
        self._calc_vscreen_size()
        return self.__vscreen_size

    def get_vscreen_normalize_offset(self) -> Tuple[int, int]:
        self._calc_vscreen_normalize_offset()
        return self.__vscreen_normalize_offset

    def add_monitor(self, monitor_model: MonitorModel):
        self.monitor_model.add(monitor_model)

    def _calc_vscreen_normalize_offset(self):
        top, left = 0, 0
        monitor: MonitorModel
        for monitor in self.monitor_model:
            if monitor.position_x < top:
                top = monitor.position_x
            if monitor.position_y < left:
                left = monitor.position_y
        self.__vscreen_normalize_offset = (top, left)

    def _calc_vscreen_size(self):
        top, left, bottom, right = 0, 0, 0, 0
        monitor: MonitorModel
        for monitor in self.monitor_model:
            if monitor.position_x < left:
                left = monitor.position_x
            if monitor.position_y < top:
                top = monitor.position_y
            if (monitor.position_x + monitor.screen_width) > right:
                right = monitor.position_x + monitor.screen_width
            if (monitor.position_y + monitor.screen_height) > bottom:
                bottom = monitor.position_y + monitor.screen_height
        self.__vscreen_size = (right - left, bottom - top)

    def _changed_monitor_model(self, new_model):
        self._calc_vscreen_normalize_offset()
        self._calc_vscreen_size()
