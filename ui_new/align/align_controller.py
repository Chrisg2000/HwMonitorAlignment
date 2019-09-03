from PySide2.QtCore import Qt

from ui_new.align.align_widget import AlignWidget
from ui_new.align.models.view_model import AlignWidgetViewModel


class AlignController:

    def __init__(self, backend):
        """Controller for the widgets on the different monitors.

        The internal model and controller is shared among all other
        widgets on the different monitors

                                Controller
            ┌─────────────   modifies models    <────────────┐
            │             and common properties              │ common
         ViewModel         │                                 │ properties
        common UI  ───┐    │                                 │ change
        properties    │    │                                 │ or general
                      ├──> ├────>   Model  ────────>  View ──┤ settings
                      │    │                                 │
                      ├──> ├────>   Model  ────────>  View ──┤
                      │    │                                 │
                      └──> └────>   Model  ────────>  View ──┘
                                 specific UI        displays
                                properties and      specific
                                     data            data


        :type backend: backend.monitor_backend.BaseMonitorBackend
        """
        self.map = {}
        self.backend = backend
        self.model = AlignWidgetViewModel(self.backend)

    def key_pressed(self, monitor, key):
        if key == Qt.Key_Escape:
            self.stop()
        elif key == Qt.Key_Up:
            monitor.position_y -= 1
        elif key == Qt.Key_Down:
            monitor.position_y += 1
        elif key == Qt.Key_M:
            monitor.monitor_name = 'Psst'
            print(monitor.monitor_name)
        else:
            return True

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
