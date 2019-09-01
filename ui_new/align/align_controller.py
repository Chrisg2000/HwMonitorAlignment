from PySide2.QtCore import Qt
from PySide2.QtWidgets import QWidget

from core.signals import Signal
from ui_new.align.align_widget import AlignWidget
from ui_new.align.align_widget_model import AlignWidgetModel


class AlignController:

    def __init__(self, backend):
        """Controller for the widgets on the different monitors.

        The internal model and controller is shared among all other
        widgets on the different monitors

        :type backend: backend.monitor_backend.BaseMonitorBackend
        """
        self.map = {}
        self.backend = backend
        self.model = AlignWidgetModel(self.backend)

    def key_pressed(self, monitor, key):
        if key == Qt.Key_Escape:
            self.stop()
        elif key == Qt.Key_Up:
            monitor.position_y -= 1
        elif key == Qt.Key_Down:
            monitor.position_y += 1

    def wheel_event(self, monitor, event):
        pass

    def start(self):
        for monitor in self.backend.monitor_model:
            widget = AlignWidget(self, self.model, monitor)
            widget.showFullScreen()

            self.map[monitor] = widget

    def stop(self):
        for widget in self.map.values():
            widget.close()
        self.map.clear()

    def button_apply(self, checked=False):
        """Align Widget Control Box Dialog Buttons Apply"""
        pass

    def button_close(self, checked=False):
        """Align Widget Control Box Dialog Buttons Close"""
        self.stop()

    def button_reset(self, checked=False):
        """Align Widget Control Box Dialog Buttons Reset"""
        pass
