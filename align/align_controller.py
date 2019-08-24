from PySide2.QtCore import Qt
from PySide2.QtGui import QMouseEvent

from backend.monitor_backend import BaseMonitorBackend
from core.has_properties import HasProperties, Property
from ui.align.align_widget import AlignWidget


class AlignController(HasProperties):
    active = Property(default=False)
    show_cursor_position = Property(default=False)
    show_diagonal_lines = Property(default=False)
    show_alignment_lines = Property(default=True)
    show_line_positions = Property(default=False)
    show_info_box = Property(default=True)
    show_circles = Property(default=False)

    def __init__(self, backend: BaseMonitorBackend):
        super().__init__()
        self.backend = backend

        self.backend.monitor_added.connect(self._monitor_model_changed)
        self.backend.monitor_removed.connect(self._monitor_model_changed)
        self.backend.monitor_model_reset.connect(self._monitor_model_changed)

        self._widget = AlignWidget(self)

    def start(self):
        self._widget.show()
        self.active = True

    def stop(self, force=False):
        self._widget.close()
        self.active = False

    def get_monitor(self, index):
        return self.backend.monitor_model.get(index)

    def key_pressed(self, key):
        if key == Qt.Key_Escape:
            self.stop()
        elif key == Qt.Key_U:
            monitor = self.backend.monitor_model.get(0)
            monitor.monitor_name = 'ABC'

    def mouse_pressed(self, event: QMouseEvent):
        for monitor in self.backend.monitor_model:
            pos = event.globalPos()
            if monitor.position_x < pos.x() < monitor.position_x + monitor.screen_width \
                    and monitor.position_y < pos.y() < monitor.position_y + monitor.screen_height:
                print(monitor)

    def _monitor_model_changed(self, *args):
        if self.active:
            self.stop(True)
            self.start()
