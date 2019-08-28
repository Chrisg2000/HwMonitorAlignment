from PySide2.QtCore import Qt
from PySide2.QtGui import QMouseEvent
from PySide2.QtWidgets import QMessageBox

from align import AdjustDirection
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
    selected_monitor = Property(default=None)

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
        elif key == Qt.Key_Up:
            self._widget_adjust(AdjustDirection.UP)
        elif key == Qt.Key_Down:
            self._widget_adjust(AdjustDirection.DOWN)

    def mouse_pressed(self, event: QMouseEvent):
        pos = event.globalPos()
        self.selected_monitor = self.backend.monitor_model.get_from_position(pos.x(), pos.y())

    def _monitor_model_changed(self, *args):
        if self.active:
            self.stop(True)
            self.start()

    def _widget_adjust(self, direction):
        if self.selected_monitor is None:
            message_box = QMessageBox(QMessageBox.Information,
                                      "Monitor selection error",
                                      "There is no monitor selected. To select an monitor move your "
                                      "cursor to the desired monitor and press left-mouse button.")
            message_box.setWindowFlag(Qt.WindowStaysOnTopHint)
            message_box.exec_()
            return
        self._widget.adjust_monitor(self.selected_monitor, direction)
