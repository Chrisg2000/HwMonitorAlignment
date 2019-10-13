from typing import Tuple

from hwmonitor.backend.backend import Backend
from hwmonitor.monitors.monitor_model import MonitorModel
from hwmonitor.vscreen.vscreen import VScreen


class Win32VScreen(VScreen):

    def __init__(self, monitors: MonitorModel, backend: Backend):
        super().__init__(monitors)
        self._backend = backend

    @property
    def primary_monitor(self):
        return next(self.monitors.filter(lambda monitor: monitor.primary))

    @property
    def monitor_order(self):
        return sorted(
            self.monitors,
            key=lambda monitor: (monitor.position_x, monitor.position_y))

    @property
    def size(self):
        return self._backend.get_vscreen_size()

    @property
    def offset(self) -> Tuple[int, int]:
        return self._backend.get_vscreen_offset()

    def get_from_position(self, x, y):
        for monitor in self.monitors:
            if monitor.position_x <= x <= monitor.position_x + monitor.screen_width and \
                    monitor.position_y <= y <= monitor.position_y + monitor.screen_height:
                return monitor
        raise LookupError("Requested position is outside of visible virtual screen area")

    def apply_changes(self):
        self._backend.set_monitor_position(None, 0, 0)
        self.layout_changed.emit()
