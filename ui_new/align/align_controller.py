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

    def start(self):
        for monitor in self.backend.monitor_model:
            widget = AlignWidget(self, self.model, monitor)
            widget.showFullScreen()

            self.map[monitor] = widget

    def stop(self):
        for widget in self.map.values():
            widget.close()
        self.map.clear()
