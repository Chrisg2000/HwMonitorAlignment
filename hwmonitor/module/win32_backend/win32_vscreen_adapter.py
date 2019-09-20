from typing import Tuple

from hwmonitor.backend.backend import Backend
from hwmonitor.monitors.vscreen_adapter import VScreenAdapter
from hwmonitor.monitors.monitor_model import MonitorModel


class Win32VScreenAdapter(VScreenAdapter):

    def __init__(self, model: MonitorModel, backend: Backend):
        super().__init__(model)

        self._backend = backend

    def get_primary_monitor(self):
        return self.model.filter(lambda monitor: monitor.primary)

    def get_monitor_order(self):
        return sorted(
            self.model,
            key=lambda monitor: (monitor.position_x, monitor.position_y)
        )

    def get_from_position(self, x, y):
        for monitor in self.model:
            if monitor.position_x <= x <= monitor.position_x + monitor.screen_width and \
                    monitor.position_y <= y <= monitor.position_y + monitor.screen_height:
                return monitor
        raise LookupError("Requested position is outside of visible virtual screen area")

    def get_vscreen_size(self):
        return self._backend.get_vscreen_size()

    def get_vscreen_normalize_offset(self) -> Tuple[int, int]:
        return self._backend.get_vscreen_normalize_offset()
