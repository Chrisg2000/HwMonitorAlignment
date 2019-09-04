from PySide2.QtCore import Qt

from ui_new.align.align_widget import AlignWidget
from ui_new.align.models.align_model import AlignModel
from ui_new.align.models.view_model import AlignViewModel


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
        self.common_model = AlignViewModel()
        self.monitor_model = self.backend.monitor_model

    def key_pressed(self, model: AlignModel, key):
        if key == Qt.Key_Escape:
            self.stop()
        elif key == Qt.Key_Up:
            model.offset -= 1
        elif key == Qt.Key_Down:
            model.offset += 1
        elif key == Qt.Key_M:
            model.monitor.monitor_name = 'Psst'
            print(model.monitor.monitor_name)
        else:
            return True

    def wheel_event(self, monitor, event):
        pass

    def start(self):
        for monitor in self.monitor_model:
            model = AlignModel(monitor, self.common_model, self.backend)
            widget = AlignWidget(self, model)
            widget.showFullScreen()

            self.map[monitor] = (model, widget)

    def stop(self):
        for _, widget in self.map.values():
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
        for model, _ in self.map.values():
            model.rollback()
